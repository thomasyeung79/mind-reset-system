"""Canonical psychology perspective reuses the secular topic rules."""

from mind_reset.content.secular.topics import TOPIC_IDS, select_topic

from .base import PerspectiveId, PerspectiveRequest, TopicId
from .catalog import CatalogPerspective


class PsychologyPerspective(CatalogPerspective):
    id = PerspectiveId("psychology")
    topics = TOPIC_IDS

    def select_topic(self, request: PerspectiveRequest) -> TopicId:
        return select_topic(request)
