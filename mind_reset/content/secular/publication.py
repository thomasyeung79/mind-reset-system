"""Version-bound evidence and fail-closed public eligibility for secular content."""

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from typing import TYPE_CHECKING, Literal
from unicodedata import normalize

if TYPE_CHECKING:
    from .catalog import CatalogEntry

ContentVersion = tuple[str, int, str]
ReviewType = Literal["editorial", "language", "mental_health_safety", "rights"]
REQUIRED_REVIEWS = frozenset(("editorial", "language", "mental_health_safety", "rights"))


@dataclass(frozen=True)
class ReviewEvidence:
    content_id: str
    revision: int
    locale: str
    perspective_id: str
    source_id: str
    source_revision: str
    content_digest: str
    review_type: ReviewType
    reviewer_id: str
    reviewed_at: date
    decision: Literal["approved", "rejected"]
    approved_scope: str
    evidence_reference: str
    rights_basis: str | None = None
    rights_holder: str | None = None
    license_or_permission_reference: str | None = None
    rights_valid_until: date | None = None


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    revision: str
    reference: str


@dataclass(frozen=True)
class PublicationPolicy:
    evidence: tuple[ReviewEvidence, ...] = ()
    sources: tuple[SourceRecord, ...] = ()
    revoked_rights: frozenset[ContentVersion] = frozenset()
    withdrawn: frozenset[ContentVersion] = frozenset()


def content_digest(text: str) -> str:
    canonical = normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def _present(*values) -> bool:
    return all(isinstance(value, str) and value.strip() for value in values)


def is_publication_eligible(
    entry: "CatalogEntry",
    *,
    policy: PublicationPolicy,
    locale: str,
    perspective_id: str,
    scope: str,
    today: date,
) -> bool:
    version = (entry.content_id, entry.revision, entry.locale)
    if (
        entry.review_status != "published"
        or entry.publication_scope != scope
        or scope != "public_reflection"
        or entry.locale != locale
        or entry.perspective_id != perspective_id
        or type(entry.revision) is not int
        or entry.revision < 1
        or type(today) is not date
        or not _present(entry.content_id, entry.text, entry.source_id, entry.source_revision)
        or version in policy.withdrawn
        or version in policy.revoked_rights
    ):
        return False

    sources = tuple(
        source for source in policy.sources
        if (source.source_id, source.revision) == (entry.source_id, entry.source_revision)
    )
    if len(sources) != 1 or not _present(sources[0].reference):
        return False

    try:
        digest = content_digest(entry.text)
    except UnicodeError:
        return False
    approved = set()
    for record in policy.evidence:
        if (
            (record.content_id, record.revision, record.locale) != version
            or type(record.revision) is not int
            or record.perspective_id != perspective_id
            or record.source_id != entry.source_id
            or record.source_revision != entry.source_revision
            or record.content_digest != digest
            or record.approved_scope != scope
        ):
            continue
        if (
            record.review_type not in REQUIRED_REVIEWS
            or record.decision != "approved"
            or type(record.reviewed_at) is not date
            or record.reviewed_at > today
            or not _present(record.reviewer_id, record.evidence_reference)
        ):
            return False
        if record.review_type == "rights":
            if not _present(record.rights_basis, record.rights_holder, record.license_or_permission_reference):
                return False
            expiry = record.rights_valid_until
            if expiry is not None and (type(expiry) is not date or expiry < today):
                return False
        approved.add(record.review_type)
    return approved == REQUIRED_REVIEWS
