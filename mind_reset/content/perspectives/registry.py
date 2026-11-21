"""Explicit registry for perspectives available to internal callers."""

from .base import Perspective, PerspectiveId
from .buddhism import BuddhismPerspective
from .christianity import ChristianityPerspective
from .psychology import PsychologyPerspective
from .taoism import TaoismPerspective


class UnknownPerspectiveError(LookupError):
    """The requested perspective has no registered adapter."""


_CANONICAL = (
    PsychologyPerspective(), ChristianityPerspective(), BuddhismPerspective(), TaoismPerspective(),
)
CANONICAL_PERSPECTIVE_IDS = tuple(perspective.id for perspective in _CANONICAL)
_PERSPECTIVES: dict[PerspectiveId, Perspective] = {
    **{perspective.id: perspective for perspective in _CANONICAL},
}


def get_perspective(perspective_id: PerspectiveId) -> Perspective:
    try:
        return _PERSPECTIVES[perspective_id]
    except KeyError:
        raise UnknownPerspectiveError(f"Unknown perspective ID: {perspective_id!r}") from None
