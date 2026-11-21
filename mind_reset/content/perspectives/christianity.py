"""Evidence-gated Christianity topics with no implicit Legacy routing."""


from .base import PerspectiveId, TopicId
from .catalog import CatalogPerspective


class ChristianityPerspective(CatalogPerspective):
    id = PerspectiveId("christianity")
    topics = (
        TopicId("faith_and_hope"),
        TopicId("prayer_and_stillness"),
        TopicId("forgiveness_and_love"),
        TopicId("facing_difficulties"),
    )
