"""Loopback-only Streamlit entry point for the four canonical perspectives."""

import streamlit as st

from mind_reset.content.perspectives.base import AvailableContent, PerspectiveRequest, UnavailableContent
from mind_reset.content.perspectives.registry import CANONICAL_PERSPECTIVE_IDS, get_perspective
from mind_reset.content.translations import EVENT_OPTIONS, MOOD_OPTIONS, TEXTS
from mind_reset.practices.breathing import generate_breathing_practice
from mind_reset.reflection.rules import generate_summary


LANGUAGES = {"zh": "中文", "en": "English", "ko": "한국어"}
COPY = {
    "perspective": ("内容视角", "Content perspective", "콘텐츠 관점"),
    "psychology": ("心理学", "Psychology", "심리학"),
    "christianity": ("基督教", "Christianity", "기독교"),
    "buddhism": ("佛法", "Buddhism", "불교"),
    "taoism": ("道教", "Taoism", "도교"),
    "stress_management": ("压力管理", "Stress management", "스트레스 관리"),
    "emotional_awareness": ("情绪觉察", "Emotional awareness", "감정 알아차리기"),
    "self_compassion": ("自我关怀", "Self-compassion", "자기 연민"),
    "sleep_relaxation": ("睡眠与放松", "Sleep and relaxation", "수면과 이완"),
    "faith_and_hope": ("信心与盼望", "Faith and hope", "믿음과 소망"),
    "prayer_and_stillness": ("祷告与安静", "Prayer and stillness", "기도와 고요"),
    "forgiveness_and_love": ("宽恕与爱", "Forgiveness and love", "용서와 사랑"),
    "facing_difficulties": ("面对困难", "Facing difficulties", "어려움에 대처하기"),
    "impermanence_and_acceptance": ("无常与接纳", "Impermanence and acceptance", "무상과 수용"),
    "compassion_and_kindness": ("慈悲与善意", "Compassion and kindness", "자비와 친절"),
    "mindfulness_and_awareness": ("正念与觉察", "Mindfulness and awareness", "정념과 알아차림"),
    "afflictions_and_wisdom": ("烦恼与智慧", "Afflictions and wisdom", "번뇌와 지혜"),
    "dao_and_nature": ("道法自然", "The Dao and naturalness", "도법자연"),
    "stillness_and_reflection": ("清静与内省", "Stillness and reflection", "청정과 성찰"),
    "softness_and_noncontention": ("柔弱不争", "Softness and noncontention", "유약과 부쟁"),
    "adapting_to_change": ("顺应变化", "Adapting to change", "변화에 맞추기"),
    "topic": ("主题", "Topic", "주제"),
    "topic_prompt": ("请选择主题", "Choose a topic", "주제를 선택하세요"),
    "topic_mode": ("选题方式", "Topic selection mode", "주제 선택 방식"),
    "auto": ("自动选题", "Automatic", "자동 선택"),
    "manual": ("手动选题", "Manual", "직접 선택"),
    "title": ("四视角 · 本地演示", "Four perspectives · Local demo", "네 가지 관점 · 로컬 데모"),
    "unavailable": ("此主题暂无获准发布的正文。", "No release-approved text is available for this topic.", "이 주제에는 공개 승인된 본문이 없습니다."),
}


def clear_session():
    for key in list(st.session_state):
        if key.startswith("four_") and key != "four_locale":
            del st.session_state[key]


def run():
    st.set_page_config(page_title="Mind Reset · Four perspectives")
    if st.get_option("server.address") != "127.0.0.1":
        st.error("This page only runs on 127.0.0.1.")
        return

    state = st.session_state
    locale = st.sidebar.selectbox(
        "Language / 语言 / 언어", tuple(LANGUAGES), format_func=LANGUAGES.__getitem__, key="four_locale",
    )
    language = LANGUAGES[locale]
    text = TEXTS[language]
    index = tuple(LANGUAGES).index(locale)
    labels = {key: values[index] for key, values in COPY.items()}
    previous = state.get("four_previous_locale", locale)
    if locale != previous:
        state.pop("four_snapshot", None)
        for field in ("perspective", "moods", "events"):
            old_key = f"four_{field}:{previous}"
            if old_key in state:
                state[f"four_{field}:{locale}"] = state.pop(old_key)
    state["four_previous_locale"] = locale

    st.title(labels["title"])
    st.caption(text["disclaimer"])
    st.warning({
        "zh": "仅限虚构签到。请勿输入真实个人、医疗或心理健康信息。",
        "en": "Use fictional check-ins only. Do not enter real personal, medical or mental health information.",
        "ko": "가상의 입력만 사용하세요. 실제 개인 정보나 의료·정신건강 정보는 입력하지 마세요.",
    }[locale])
    perspective = st.selectbox(
        labels["perspective"], CANONICAL_PERSPECTIVE_IDS, key=f"four_perspective:{locale}",
        format_func=labels.__getitem__,
    )
    adapter = get_perspective(perspective)
    selection_scope = (perspective, locale)
    if selection_scope != state.get("four_selection_scope"):
        for key in list(state):
            if key.startswith(("four_topic:", "four_topic_mode:")):
                del state[key]
        state["four_selection_scope"] = selection_scope

    mode = "manual"
    if perspective == "psychology":
        mode = st.radio(
            labels["topic_mode"], ("auto", "manual"), format_func=labels.__getitem__,
            key=f"four_topic_mode:{locale}", horizontal=True,
        )

    manual_topic = None
    if mode == "manual":
        manual_topic = st.selectbox(
            labels["topic"], adapter.topics, index=None, placeholder=labels["topic_prompt"],
            format_func=labels.__getitem__, key=f"four_topic:{perspective}:{locale}",
        )

    moods = st.multiselect(text["mood"], tuple(MOOD_OPTIONS),
                           format_func=lambda value: MOOD_OPTIONS[value][language], key=f"four_moods:{locale}")
    events = st.multiselect(text["things"], tuple(EVENT_OPTIONS),
                            format_func=lambda value: EVENT_OPTIONS[value][language], key=f"four_events:{locale}")
    stress = st.slider(text["stress"], 1, 4, 1, key="four_stress")
    energy = st.slider(text["energy"], 1, 4, 3, key="four_energy")
    scope = (perspective, locale, mode, manual_topic, tuple(moods), tuple(events), stress, energy)
    if scope != state.get("four_scope"):
        state["four_scope"] = scope
        state.pop("four_snapshot", None)

    st.button(text["clear_session"], key="four_clear", on_click=clear_session)
    view = st.radio(
        "Dashboard / Story Mode", ("dashboard", "story_mode"), format_func=text.__getitem__,
        key=f"four_view:{locale}", horizontal=True, label_visibility="collapsed",
    )
    if st.button(text["button"], key="four_generate", disabled=mode == "manual" and manual_topic is None):
        if not moods and not events:
            st.error(text["error"])
        else:
            breathing_type = generate_breathing_practice(moods, stress, energy, language)["type"]
            request = PerspectiveRequest(
                locale, tuple(moods), tuple(events), stress, energy, breathing_type, manual_topic=manual_topic,
            )
            state["four_snapshot"] = (
                generate_summary(moods, events, stress, energy, language), adapter.generate(request),
            )

    if "four_snapshot" not in state:
        return
    summary, result = state["four_snapshot"]
    if (
        result.perspective_id != perspective or result.language != locale
        or result.topic_id not in adapter.topics
        or (mode == "manual" and result.topic_id != manual_topic)
    ):
        state.pop("four_snapshot", None)
        return
    st.subheader(labels[perspective])
    st.caption(labels[result.topic_id])
    if view == "dashboard":
        st.subheader(text["insight"])
        st.info(summary)
    else:
        st.markdown(f"**{text['insight']}**\n\n{summary}")
    if isinstance(result, AvailableContent) and adapter.is_current(result):
        for block in result.blocks:
            st.write(block.text)
            st.caption(f"{block.source.source_id} · {block.source.locator}")
    else:
        # Remove an invalidated body so that changing views cannot restore it.
        if isinstance(result, AvailableContent):
            state["four_snapshot"] = (
                summary, UnavailableContent(perspective, locale, "missing_content", result.topic_id),
            )
        st.info(labels["unavailable"])


if __name__ == "__main__":
    run()
