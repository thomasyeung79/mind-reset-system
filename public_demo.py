"""Read-only public demo for the anonymous Community Cloud candidate."""

import streamlit as st

from mind_reset.content.perspectives.base import PerspectiveRequest
from mind_reset.content.perspectives.registry import CANONICAL_PERSPECTIVE_IDS, get_perspective
from mind_reset.content.translations import TEXTS
from mind_reset.reflection.rules import generate_summary
from perspective_app import BRAND_NAME, COPY, LANGUAGES


NOTICE = (
    "这是只读的虚构签到示例，供教育和界面演示使用，不提供医疗服务。本站没有签到输入框；托管平台可能记录访问和用量信息。",
    "This read-only fictional check-in is an educational interface demo. It provides no medical service or check-in form. The hosting platform may log visits and usage.",
    "가상의 체크인을 보여 주는 읽기 전용 교육용 데모입니다. 의료 서비스나 체크인 입력란은 제공하지 않습니다. 호스팅 플랫폼이 방문 및 사용 정보를 기록할 수 있습니다.",
)
UNAVAILABLE = "The public demonstration is unavailable."


def demo_topics():
    """Evaluate fixed requests through the gate and keep only the decision."""
    topics = {}
    for view in CANONICAL_PERSPECTIVE_IDS:
        adapter = get_perspective(view)
        for locale in LANGUAGES:
            topics[locale, view] = [
                (topic, result_is_available(adapter, locale, topic))
                for topic in adapter.topics
            ]
    return topics


def result_is_available(adapter, locale, topic):
    request = PerspectiveRequest(locale, ("Calm",), (), 1, 3, "basic", topic)
    result = adapter.generate(request)
    return result.status == "available" and adapter.is_current(result)


def run():
    st.set_page_config(page_title=BRAND_NAME)
    if (
        st.get_option("server.enableCORS") is not True
        or st.get_option("client.showErrorDetails") not in ("none", False)
    ):
        st.error(UNAVAILABLE)
        return

    try:
        topics = demo_topics()
    except Exception:
        st.error(UNAVAILABLE)
        return

    st.title(BRAND_NAME)
    for index, ((locale, language), pane) in enumerate(
        zip(LANGUAGES.items(), st.tabs(list(LANGUAGES.values()), on_change="ignore"))
    ):
        with pane:
            st.markdown(COPY["tagline"][index])
            st.caption(NOTICE[index])
            labels = TEXTS[language]
            summary = generate_summary(("Calm",), (), 1, 3, language)
            views = [COPY[view][index] for view in CANONICAL_PERSPECTIVE_IDS]
            for view, panel in zip(CANONICAL_PERSPECTIVE_IDS, st.tabs(views, on_change="ignore")):
                with panel:
                    dashboard, story = st.tabs(
                        (labels["dashboard"], labels["story_mode"]), on_change="ignore",
                    )
                    for section in (dashboard, story):
                        section.markdown(summary)
                        for topic, released in topics[locale, view]:
                            section.markdown(f"**{COPY[topic][index]}**")
                            if released:
                                section.caption((
                                    "只读演示省略获准发布的正文。",
                                    "Released text is omitted in this read-only demo.",
                                    "이 읽기 전용 데모에서는 공개 승인된 본문을 생략합니다.",
                                )[index])
                            else:
                                section.caption(COPY["unavailable"][index])


if __name__ == "__main__":
    run()
