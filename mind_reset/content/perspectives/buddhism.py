"""Buddhism catalog. Release-approved content has not been supplied."""

from .base import PerspectiveId, TopicId
from .catalog import CatalogPerspective


class BuddhismPerspective(CatalogPerspective):
    id = PerspectiveId("buddhism")
    topics = (
        TopicId("impermanence_and_acceptance"),
        TopicId("compassion_and_kindness"),
        TopicId("mindfulness_and_awareness"),
        TopicId("afflictions_and_wisdom"),
    )
    legacy_topics = (TopicId("buddhism_overview"),)
