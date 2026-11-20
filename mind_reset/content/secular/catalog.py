"""Public catalog. No entries have release evidence in this snapshot."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Literal

from mind_reset.content.perspectives.base import LanguageCode, PerspectiveId, TopicId

from .publication import PublicationPolicy, is_publication_eligible


SECULAR_ID = PerspectiveId("secular")
LANGUAGES: tuple[LanguageCode, ...] = ("zh", "en", "ko")
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



PUBLICATION_POLICY = PublicationPolicy()
CATALOG: Mapping[tuple[TopicId, LanguageCode], CatalogEntry] = MappingProxyType({})


def get_entry(
    topic: TopicId, locale: LanguageCode
) -> CatalogEntry | None:
    entry = CATALOG.get((topic, locale))
    if (
        entry is None
        or entry.perspective_id != SECULAR_ID
        or entry.topic_id != topic
        or entry.locale != locale
        or not isinstance(entry.text, str)
        or not entry.text.strip()
        or not isinstance(entry.source_id, str)
        or not entry.source_id.strip()
        or not isinstance(entry.content_id, str)
        or not entry.content_id.strip()
        or type(entry.revision) is not int
        or entry.revision < 1
        or (entry.content_id, entry.revision, entry.locale) in PUBLICATION_POLICY.withdrawn
        or (entry.content_id, entry.revision, entry.locale) in PUBLICATION_POLICY.revoked_rights
    ):
        return None
    if is_publication_eligible(
        entry, policy=PUBLICATION_POLICY, locale=locale, perspective_id=SECULAR_ID,
        scope="public_reflection", today=datetime.now(timezone.utc).date(),
    ):
        return entry
    return None
