"""Secular perspective for evidence-backed public content."""

from mind_reset.content.secular.catalog import LANGUAGES, SECULAR_ID, get_entry
from mind_reset.content.secular.topics import select_topic

from .base import (
    AvailableContent,
    ContentBlock,
    PerspectiveRequest,
    PerspectiveResult,
    SourceReference,
    UnavailableContent,
)


class SecularPerspective:
    id = SECULAR_ID

    def generate(self, request: PerspectiveRequest) -> PerspectiveResult:
        topic = select_topic(request)
        language = request.language
        if language not in LANGUAGES:
            return UnavailableContent(self.id, language, "unsupported_language", topic)

        entry = get_entry(topic, language)
        if entry is None:
            return UnavailableContent(self.id, language, "missing_content", topic)

        source = SourceReference(entry.source_id, f"{entry.content_id}@{entry.revision}", language)
        block = ContentBlock(entry.content_type, entry.text, source)
        return AvailableContent(self.id, language, topic, (block,))


def is_current_result(content: AvailableContent) -> bool:
    """Check the stored text and locator against the currently eligible entry."""
    if content.perspective_id != SECULAR_ID or len(content.blocks) != 1:
        return False
    entry = get_entry(content.topic_id, content.language)
    if entry is None:
        return False
    block = content.blocks[0]
    return (
        block.kind == entry.content_type
        and block.text == entry.text
        and block.source == SourceReference(
            entry.source_id, f"{entry.content_id}@{entry.revision}", entry.locale,
        )
    )
