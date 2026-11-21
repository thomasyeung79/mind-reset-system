"""Catalog entry types for the four-perspective demonstration."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from mind_reset.content.perspectives.base import LanguageCode, PerspectiveId, TopicId

PublicationScope = Literal["internal", "public_reflection"]


class ReviewStatus(str, Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"


@dataclass(frozen=True)
class CatalogEntry:
    content_id: str
    revision: int
    locale: LanguageCode
    perspective_id: PerspectiveId
    topic_id: TopicId
    text: str
    content_type: Literal["reflection_practice"]
    source_id: str
    review_status: ReviewStatus
    publication_scope: PublicationScope
    source_revision: str | None = None
