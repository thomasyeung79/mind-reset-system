"""Taoism catalog. Release-approved content has not been supplied."""

from .base import PerspectiveId, TopicId
from .catalog import CatalogPerspective


class TaoismPerspective(CatalogPerspective):
    id = PerspectiveId("taoism")
    topics = (
        TopicId("dao_and_nature"),
        TopicId("stillness_and_reflection"),
        TopicId("softness_and_noncontention"),
        TopicId("adapting_to_change"),
    )
    legacy_topics = (TopicId("taoism_overview"),)
