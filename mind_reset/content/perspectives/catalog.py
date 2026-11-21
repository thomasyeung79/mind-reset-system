"""Shared publication gate for the canonical perspectives."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType

from mind_reset.content.secular.catalog import CatalogEntry
from mind_reset.content.secular.publication import PublicationPolicy, is_publication_eligible

from .base import (
    AvailableContent, ContentBlock, LanguageCode, PerspectiveId, PerspectiveRequest,
    PerspectiveResult, SourceReference, TopicId, UnavailableContent,
)


class UnknownPerspectiveTopicError(LookupError):
    """The manual topic does not belong to this perspective."""


@dataclass(frozen=True)
class PerspectiveCatalog:
    entries: Mapping[tuple[TopicId, LanguageCode], CatalogEntry] = field(
        default_factory=lambda: MappingProxyType({})
    )
    policy: PublicationPolicy = field(default_factory=PublicationPolicy)


class CatalogPerspective:
    """Render only exact-locale content with valid evidence for this perspective."""

    id: PerspectiveId
    topics: tuple[TopicId, ...]
    legacy_topics: tuple[TopicId, ...] = ()

    def __init__(self, catalog: PerspectiveCatalog | None = None):
        self.catalog = catalog if catalog is not None else PerspectiveCatalog()

    def select_topic(self, request: PerspectiveRequest) -> TopicId | None:
        return None

    def _published(self, topic: TopicId, locale: LanguageCode) -> AvailableContent | None:
        entry = self.catalog.entries.get((topic, locale))
        if topic not in self.topics or entry is None or entry.topic_id != topic:
            return None
        if not is_publication_eligible(
            entry, policy=self.catalog.policy, locale=locale, perspective_id=self.id,
            scope="public_reflection", today=datetime.now(timezone.utc).date(),
        ):
            return None
        source = SourceReference(entry.source_id, f"{entry.content_id}@{entry.revision}", locale)
        return AvailableContent(self.id, locale, topic, (ContentBlock(entry.content_type, entry.text, source),))

    def generate(self, request: PerspectiveRequest) -> PerspectiveResult:
        if request.language not in ("zh", "en", "ko"):
            return UnavailableContent(self.id, request.language, "unsupported_language")
        topic = request.manual_topic if request.manual_topic is not None else self.select_topic(request)
        if topic is None or topic in self.legacy_topics:
            return UnavailableContent(self.id, request.language, "missing_content", topic)
        if topic not in self.topics:
            raise UnknownPerspectiveTopicError(f"Unknown topic for {self.id}: {topic!r}")
        result = self._published(topic, request.language)
        if result is None:
            return UnavailableContent(self.id, request.language, "missing_content", topic)
        return result

    def is_current(self, result: AvailableContent) -> bool:
        return (
            result.perspective_id == self.id
            and result.topic_id in self.topics
            and self._published(result.topic_id, result.language) == result
        )
