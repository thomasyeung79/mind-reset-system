"""Verify the public demo does not accept a check-in or render catalog bodies."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

from mind_reset.content.perspectives.base import PerspectiveRequest
from mind_reset.content.perspectives.catalog import PerspectiveCatalog
from mind_reset.content.perspectives.registry import get_perspective
from mind_reset.content.secular.catalog import CatalogEntry, ReviewStatus
from public_demo import NOTICE, UNAVAILABLE, demo_topics


APP = Path(__file__).resolve().parents[1] / "public_demo.py"


class ReadOnlyDemoTests(unittest.TestCase):
    def test_platform_simulation_displays_all_topics_without_input(self):
        original = st.get_option
        overrides = {"server.enableXsrfProtection": False, "browser.gatherUsageStats": True}

        def option(key):
            return overrides[key] if key in overrides else original(key)

        with patch.object(st, "get_option", side_effect=option):
            app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        for kind in (
            "text_input", "text_area", "file_uploader", "button", "form", "selectbox",
            "multiselect", "slider", "radio", "download_button", "chat_input",
        ):
            self.assertFalse(app.get(kind), kind)
        self.assertTrue(all(notices in [node.value for node in app.caption] for notices in NOTICE))
        topics = demo_topics()
        self.assertEqual(len(topics), 12)
        self.assertEqual(sum(map(len, topics.values())), 48)
        self.assertTrue(all(not released for group in topics.values() for _, released in group))
        self.assertNotIn("four_snapshot", app.session_state)

    def test_draft_and_unproven_published_content_are_rejected(self):
        adapter = get_perspective("christianity")
        topic = adapter.topics[0]
        for status, scope in ((ReviewStatus.DRAFT, "internal"), (ReviewStatus.PUBLISHED, "public_reflection")):
            with self.subTest(status=status):
                marker = "SYNTHETIC_BODY_SHOULD_NOT_RENDER"
                entry = CatalogEntry("fixture", 1, "zh", "christianity", topic, marker,
                                     "reflection_practice", "test.source", status, scope, "fixture")
                candidate = type(adapter)(PerspectiveCatalog({(topic, "zh"): entry}))

                def get(view):
                    return candidate if view == "christianity" else get_perspective(view)

                with patch("mind_reset.content.perspectives.registry.get_perspective", side_effect=get) as lookup:
                    app = AppTest.from_file(str(APP)).run()
                    lookup.assert_any_call("christianity")
                self.assertEqual(candidate.generate(PerspectiveRequest("zh", ("Calm",), (), 1, 3, "basic", topic)).status, "unavailable")
                self.assertNotIn(marker, repr(app))
                self.assertFalse(app.exception)

    def test_error_response_does_not_display_or_log_internal_detail(self):
        output = StringIO()
        marker = "SYNTHETIC_INTERNAL_ERROR_DETAIL"
        with (
            patch("mind_reset.content.perspectives.registry.get_perspective", side_effect=RuntimeError(marker)),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        self.assertEqual([error.value for error in app.error], [UNAVAILABLE])
        self.assertFalse(app.get("tab"))
        self.assertNotIn(marker, output.getvalue())

    def test_unsafe_cors_or_error_detail_refuses_render(self):
        original = st.get_option
        for bad_key, bad_value in (("server.enableCORS", False), ("client.showErrorDetails", "full")):
            with self.subTest(option=bad_key):
                def option(key):
                    return bad_value if key == bad_key else original(key)

                with patch.object(st, "get_option", side_effect=option):
                    app = AppTest.from_file(str(APP)).run()
                self.assertFalse(app.exception)
                self.assertEqual([error.value for error in app.error], [UNAVAILABLE])
                self.assertFalse(app.get("tab"))
