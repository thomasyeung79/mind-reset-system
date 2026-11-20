import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from mind_reset.content.perspectives.base import PerspectiveRequest, UnavailableContent
from mind_reset.content.perspectives.registry import UnknownPerspectiveError, get_perspective
from mind_reset.content.secular.catalog import CATALOG, PUBLICATION_POLICY


APP = Path(__file__).resolve().parents[1] / "main.py"


class PublicSnapshotTests(unittest.TestCase):
    def test_public_catalog_has_no_evidence_or_text(self):
        self.assertFalse(CATALOG)
        self.assertFalse(PUBLICATION_POLICY.evidence)
        adapter = get_perspective("secular")
        self.assertFalse(hasattr(adapter, "preview_draft"))
        for locale in ("zh", "en", "ko"):
            result = adapter.generate(PerspectiveRequest(locale, ("Calm",), (), 1, 3, "basic"))
            self.assertIsInstance(result, UnavailableContent)
        with self.assertRaises(UnknownPerspectiveError):
            get_perspective("christian")

    def test_dashboard_story_and_three_languages(self):
        app = AppTest.from_file(str(APP)).run()
        choices = (
            ("zh", "暂无获准发布的主题正文。", "这次虚构签到选择了以下主题。"),
            ("en", "No release-approved text is available.", "This fictional check-in was matched to the topic below."),
            ("ko", "공개 승인된 주제 본문이 없습니다.", "이 가상의 체크인은 아래 주제와 연결되었습니다."),
        )
        for locale, unavailable, story in choices:
            app.sidebar.selectbox(key="language").select(locale).run()
            self.assertNotIn("snapshot", app.session_state)
            app.selectbox(key=f"topic:{locale}").select("self_compassion")
            app.button(key="generate").click().run()
            self.assertFalse(app.exception)
            snapshot = app.session_state["snapshot"]
            self.assertEqual(snapshot.content.topic_id, "self_compassion")
            self.assertIn(unavailable, [item.value for item in app.info])
            self.assertEqual(len(app.metric), 2)
            app.radio(key=f"view:{locale}").set_value("story").run()
            self.assertFalse(app.exception)
            self.assertIs(app.session_state["snapshot"], snapshot)
            self.assertIn(story, [item.value for item in app.markdown])

    def test_separate_sessions_and_clear(self):
        a = AppTest.from_file(str(APP)).run()
        b = AppTest.from_file(str(APP)).run()
        a.button(key="generate").click().run()
        self.assertNotIn("snapshot", b.session_state)
        b.button(key="generate").click().run()
        saved = b.session_state["snapshot"]
        a.button(key="clear").click().run()
        self.assertFalse(a.exception)
        self.assertNotIn("snapshot", a.session_state)
        self.assertIs(b.session_state["snapshot"], saved)
