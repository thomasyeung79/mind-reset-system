"""Explicit registry for perspectives available to the public interface."""

from .base import Perspective, PerspectiveId
from .secular import SecularPerspective


class UnknownPerspectiveError(LookupError):
    """The requested perspective has no registered adapter."""


_secular = SecularPerspective()
_PERSPECTIVES: dict[PerspectiveId, Perspective] = {
    _secular.id: _secular,
}


def get_perspective(perspective_id: PerspectiveId) -> Perspective:
    try:
        return _PERSPECTIVES[perspective_id]
    except KeyError:
        raise UnknownPerspectiveError(f"Unknown perspective ID: {perspective_id!r}") from None
