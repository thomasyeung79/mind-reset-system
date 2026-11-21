"""Stable secular topic IDs and rules based on the current check-in."""

from mind_reset.content.perspectives.base import PerspectiveRequest, TopicId


STRESS_MANAGEMENT = TopicId("stress_management")
EMOTIONAL_AWARENESS = TopicId("emotional_awareness")
SELF_COMPASSION = TopicId("self_compassion")
SLEEP_RELAXATION = TopicId("sleep_relaxation")

TOPIC_IDS = (STRESS_MANAGEMENT, EMOTIONAL_AWARENESS, SELF_COMPASSION, SLEEP_RELAXATION)


class UnknownSecularTopicError(LookupError):
    """A manual topic does not belong to the secular perspective."""


def select_topic(request: PerspectiveRequest) -> TopicId:
    if request.manual_topic is not None:
        if request.manual_topic not in TOPIC_IDS:
            raise UnknownSecularTopicError(f"Unknown secular topic ID: {request.manual_topic!r}")
        return request.manual_topic
    if request.stress >= 3 or request.breathing_type == "calming":
        return STRESS_MANAGEMENT
    if "Angry" in request.moods or "Argued with someone" in request.events or request.breathing_type == "pause":
        return EMOTIONAL_AWARENESS
    if "Low" in request.moods or "Numb" in request.moods:
        return SELF_COMPASSION
    if "Tired" in request.moods or request.energy <= 2 or request.breathing_type == "recovery":
        return SLEEP_RELAXATION
    return EMOTIONAL_AWARENESS
