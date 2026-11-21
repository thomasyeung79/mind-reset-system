"""Regression tests for the standalone four-perspective public demo."""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from mind_reset.content.perspectives.base import PerspectiveRequest
from mind_reset.content.perspectives.catalog import PerspectiveCatalog
from mind_reset.content.perspectives.registry import CANONICAL_PERSPECTIVE_IDS, get_perspective
from mind_reset.content.secular.catalog import CatalogEntry, ReviewStatus
from perspective_app import COPY

ROOT = Path(__file__).resolve().parents[1]


class PublicDemoTests(unittest.TestCase):
    def test_all_topics_in_three_languages(self):
        views = ("psychology", "christianity", "buddhism", "taoism")
        self.assertEqual(tuple(CANONICAL_PERSPECTIVE_IDS), views)
        app = AppTest.from_file(str(ROOT / "perspective_app.py")).run()
        for index, locale in enumerate(("zh", "en", "ko")):
            app.sidebar.selectbox(key="four_locale").select(locale).run()
            selection = app.selectbox(key=f"four_perspective:{locale}")
            self.assertEqual(selection.options, [COPY[view][index] for view in views])
            for view in views:
                app.selectbox(key=f"four_perspective:{locale}").select(view).run()
                if view == "psychology":
                    app.radio(key=f"four_topic_mode:{locale}").set_value("manual").run()
                topics = get_perspective(view).topics
                widget = app.selectbox(key=f"four_topic:{view}:{locale}")
                self.assertEqual(widget.options, [COPY[topic][index] for topic in topics])
                self.assertEqual(len(topics), 4)
                self.assertFalse(app.exception)

    def test_empty_catalog_and_reject_missing_evidence(self):
        for view in CANONICAL_PERSPECTIVE_IDS:
            adapter = get_perspective(view)
            self.assertFalse(adapter.catalog.entries)
            for topic in adapter.topics:
                for locale in ("zh", "en", "ko"):
                    request = PerspectiveRequest(locale, (), (), 1, 1, "calm", topic)
                    self.assertEqual(adapter.generate(request).status, "unavailable")
                    for state, scope in ((ReviewStatus.DRAFT, "internal"), (ReviewStatus.PUBLISHED, "public_reflection")):
                        entry = CatalogEntry(
                            "synthetic.test", 1, locale, view, topic, "Synthetic fixture",
                            "reflection_practice", "synthetic.source", state, scope, "fixture",
                        )
                        test_adapter = type(adapter)(PerspectiveCatalog({(topic, locale): entry}))
                        self.assertEqual(test_adapter.generate(request).status, "unavailable")

    def test_compatibility_entry_and_session_isolation(self):
        first = AppTest.from_file(str(ROOT / "main.py")).run()
        first.multiselect(key="four_moods:zh").select("Anxious").run()
        first.button(key="four_generate").click().run()
        self.assertFalse(first.exception)
        snapshot = first.session_state["four_snapshot"]
        first.radio(key="four_view:zh").set_value("story_mode").run()
        self.assertIs(first.session_state["four_snapshot"], snapshot)

        second = AppTest.from_file(str(ROOT / "perspective_app.py")).run()
        self.assertEqual(second.multiselect(key="four_moods:zh").value, [])
        self.assertNotIn("four_snapshot", second.session_state)
        first.slider(key="four_stress").set_value(4).run()
        self.assertNotIn("four_snapshot", first.session_state)
        first.button(key="four_generate").click().run()
        first.button(key="four_clear").click().run()
        self.assertNotIn("four_snapshot", first.session_state)


if __name__ == "__main__":
    unittest.main()
