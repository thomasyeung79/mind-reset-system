"""Public reflection interface with fictional selections."""

from dataclasses import dataclass, replace

import streamlit as st

from mind_reset.content.perspectives.base import AvailableContent, PerspectiveRequest, UnavailableContent
from mind_reset.content.perspectives.registry import get_perspective
from mind_reset.content.perspectives.secular import is_current_result
from mind_reset.content.secular.topics import TOPIC_IDS
from mind_reset.content.translations import EVENT_OPTIONS, MOOD_OPTIONS


LANGUAGES = {"zh": "中文", "en": "English", "ko": "한국어"}
LABELS = {
    "title": ("身心反思 · 演示", "Mind Reset · Demo", "마음 돌아보기 · 데모"),
    "notice": (
        "请使用虚构输入。本演示仅供一般反思，不提供诊断或治疗。结果仅保存在当前会话。",
        "Use fictional inputs. This demo is for general reflection and offers no diagnosis or treatment. Results stay in this session.",
        "가상의 입력을 사용해 주세요. 일반적인 성찰용 데모이며 진단이나 치료를 제공하지 않습니다. 결과는 현재 세션에만 남습니다.",
    ),
    "mood": ("演示情绪", "Sample mood", "예시 감정"),
    "event": ("演示事件", "Sample event", "예시 사건"),
    "energy": ("能量", "Energy", "에너지"),
    "stress": ("压力", "Stress", "스트레스"),
    "perspective": ("内容视角 · 世俗反思", "Perspective · Secular reflection", "콘텐츠 관점 · 세속적 성찰"),
    "topic": ("主题选择", "Topic selection", "주제 선택"),
    "auto": ("自动选题", "Automatic topic", "자동 주제"),
    "generate": ("生成演示结果", "Generate demo result", "데모 결과 생성"),
    "clear": ("清除会话", "Clear session", "세션 지우기"),
    "view": ("结果视图", "Result view", "결과 보기"),
    "dashboard": ("仪表盘", "Dashboard", "대시보드"),
    "story": ("故事模式", "Story Mode", "스토리 모드"),
    "story_intro": (
        "这次虚构签到选择了以下主题。",
        "This fictional check-in was matched to the topic below.",
        "이 가상의 체크인은 아래 주제와 연결되었습니다.",
    ),
    "matched": ("匹配主题", "Matched topic", "선택된 주제"),
    "unavailable": ("暂无获准发布的主题正文。", "No release-approved text is available.", "공개 승인된 주제 본문이 없습니다."),
    "example_title": ("界面演示示例", "Interface example", "인터페이스 예시"),
    "example": (
        "示例人物用一个圆点标记卡片，方便稍后辨认。",
        "The fictional participant marks a card with a dot so it is easy to recognize later.",
        "예시 속 인물은 나중에 알아보기 쉽도록 카드에 점을 표시합니다.",
    ),
    "breathing": ("可选呼吸演示", "Optional breathing demo", "선택형 호흡 데모"),
    "breath_example": (
        "如果觉得自在，可以短暂留意一次自然呼吸。你可以跳过，或随时停止。",
        "If comfortable, notice one natural breath. You can skip this or stop whenever you like.",
        "편안하다면 자연스러운 호흡을 한 번 느껴 보세요. 건너뛰거나 언제든 멈춰도 됩니다.",
    ),
    "stress_management": ("压力调节", "Stress management", "스트레스 조절"),
    "emotional_awareness": ("情绪觉察", "Emotional awareness", "감정 알아차리기"),
    "self_compassion": ("自我关怀", "Self-compassion", "자기 연민"),
    "sleep_relaxation": ("休息与放松", "Rest and relaxation", "휴식과 이완"),
}


@dataclass(frozen=True)
class Snapshot:
    stress: int
    energy: int
    content: AvailableContent | UnavailableContent


def clear_session():
    for key in list(st.session_state):
        if key != "language":
            del st.session_state[key]


def run():
    st.set_page_config(page_title="Mind Reset · Demo")
    state = st.session_state
    locale = st.sidebar.selectbox("Language / 语言 / 언어", tuple(LANGUAGES),
                                  format_func=LANGUAGES.__getitem__, key="language")
    labels = {key: values[tuple(LANGUAGES).index(locale)] for key, values in LABELS.items()}
    previous = state.get("result_locale", locale)
    if previous != locale:
        state.pop("snapshot", None)
        for key in ("mood", "event", "topic"):
            old = f"{key}:{previous}"
            if old in state:
                state[f"{key}:{locale}"] = state.pop(old)
    state["result_locale"] = locale
    st.title(labels["title"])
    st.caption(labels["notice"])
    language = LANGUAGES[locale]
    mood = st.selectbox(labels["mood"], tuple(MOOD_OPTIONS),
                        format_func=lambda key: MOOD_OPTIONS[key][language], key=f"mood:{locale}")
    event = st.selectbox(labels["event"], tuple(EVENT_OPTIONS),
                         format_func=lambda key: EVENT_OPTIONS[key][language], key=f"event:{locale}")
    stress = st.slider(labels["stress"], 1, 4, 1, key="stress")
    energy = st.slider(labels["energy"], 1, 4, 3, key="energy")
    st.caption(labels["perspective"])
    topic = st.selectbox(labels["topic"], ("auto", *TOPIC_IDS),
                         format_func=labels.__getitem__, key=f"topic:{locale}")
    if state.get("result_topic") != topic:
        state.pop("snapshot", None)
    state["result_topic"] = topic
    st.button(labels["clear"], key="clear", on_click=clear_session)
    if st.button(labels["generate"], key="generate"):
        request = PerspectiveRequest(locale, (mood,), (event,), stress, energy, "basic",
                                     None if topic == "auto" else topic)
        state["snapshot"] = Snapshot(stress, energy, get_perspective("secular").generate(request))
    view = st.radio(labels["view"], ("dashboard", "story"),
                    format_func=labels.__getitem__, key=f"view:{locale}", horizontal=True)
    snapshot = state.get("snapshot")
    if snapshot is None:
        return
    content = snapshot.content
    if isinstance(content, AvailableContent) and not is_current_result(content):
        content = UnavailableContent(content.perspective_id, content.language, "missing_content", content.topic_id)
        state["snapshot"] = snapshot = replace(snapshot, content=content)
    if view == "dashboard":
        columns = st.columns(2)
        columns[0].metric(labels["stress"], snapshot.stress)
        columns[1].metric(labels["energy"], snapshot.energy)
    else:
        st.write(labels["story_intro"])
    st.subheader(labels["matched"])
    st.write(labels[content.topic_id])
    if isinstance(content, AvailableContent):
        for block in content.blocks:
            st.write(block.text)
            st.caption(f"{block.source.source_id} · {block.source.locator}")
    else:
        st.info(labels["unavailable"])
    st.subheader(labels["example_title"])
    st.write(labels["example"])
    with st.expander(labels["breathing"]):
        st.write(labels["breath_example"])
