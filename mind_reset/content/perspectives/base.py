"""Shared contract for internal content perspective adapters."""

from dataclasses import dataclass
from typing import ClassVar, Literal, NewType, Protocol


PerspectiveId = NewType("PerspectiveId", str)
TopicId = NewType("TopicId", str)
LanguageCode = Literal["zh", "en", "ko"]


@dataclass(frozen=True)
class PerspectiveRequest:
    language: LanguageCode
    moods: tuple[str, ...]
    events: tuple[str, ...]
    stress: int
    energy: int
    breathing_type: str
    manual_topic: TopicId | None = None


@dataclass(frozen=True)
class SourceReference:
    source_id: str
    locator: str
    language: LanguageCode
    # A legacy locator identifies source material without certifying its edition.
    edition_id: str | None = None


@dataclass(frozen=True)
class ContentBlock:
    kind: str
    text: str
    source: SourceReference


@dataclass(frozen=True)
class AvailableContent:
    status: ClassVar[Literal["available"]] = "available"
    perspective_id: PerspectiveId
    language: LanguageCode
    topic_id: TopicId
    blocks: tuple[ContentBlock, ...]


@dataclass(frozen=True)
class UnavailableContent:
    status: ClassVar[Literal["unavailable"]] = "unavailable"
    perspective_id: PerspectiveId
    language: LanguageCode
    reason: Literal["unsupported_language", "missing_content"]
    topic_id: TopicId | None = None


PerspectiveResult = AvailableContent | UnavailableContent


class Perspective(Protocol):
    @property
    def id(self) -> PerspectiveId: ...

    def generate(self, request: PerspectiveRequest) -> PerspectiveResult: ...
