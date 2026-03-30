import streamlit as st

st.title("🫀 Mind Reset System")
st.caption("A small system for heavy days.")
st.markdown("---")

things_happened_options = [
    "A. Failed the exam again",
    "B. Had a long day",
    "C. Argued with someone",
    "D. Nothing special",
]

things_happened = st.multiselect("Current things", things_happened_options)
clean_things = [m.split(".", 1)[1].strip() for m in things_happened]

st.markdown("---")

mood_options = [
    "A. Low",
    "B. Tired",
    "C. Anxious",
    "D. Angry",
    "E. Numb",
    "F. Calm",
]

mood = st.multiselect("Current mood", mood_options)
clean_mood = [m.split(".", 1)[1].strip() for m in mood]

st.markdown("---")

energy_level = st.selectbox(
        "Energy level:",
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 - Exhausted",
            2: "2 - Normal",
            3: "3 - Good",
            4: "4 - Very energetic",
        }[x]
    )

st.markdown("---")

stress_level = st.selectbox(
        "Stress level:",
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 - Relaxed",
            2: "2 - Manageable",
            3: "3 - High pressure",
            4: "4 - Overwhelmed",
        }[x]
    )

st.markdown("---")


def format_phrase(items):
    if len(items) == 0:
        return ""
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return f"{', '.join(items[:-1])} and {items[-1]}"

def generate_summary(clean_mood, clean_things, stress_level, energy_level):

    mood_parts = []
    event_parts = []

    # 🧠 Mood（情绪）
    if "Tired" in clean_mood:
        mood_parts.append("mentally tired")
    elif "Numb" in clean_mood:
        mood_parts.append("emotionally numb")
    elif "Anxious" in clean_mood:
        mood_parts.append("anxious")
    elif "Angry" in clean_mood:
        mood_parts.append("irritated")
    elif "Low" in clean_mood:
        mood_parts.append("low")
    elif "Calm" in clean_mood:
        mood_parts.append("relatively calm")

    # 📉 Things happened（事件）
    if "Failed the exam again" in clean_things:
        event_parts.append("after a setback")
    if "Had a long day" in clean_things:
        event_parts.append("after a long day")
    if "Argued with someone" in clean_things:
        event_parts.append("after a conflict")
    if "Nothing special" in clean_things:
        event_parts.append("with no major events today")

    # 🔥 Stress + Energy（核心状态）
    if stress_level == 4 and energy_level == 1:
        core = "You are overwhelmed and exhausted."
    elif stress_level >= 3 and energy_level <= 2:
        core = "You are under pressure and feeling drained."
    elif stress_level >= 3:
        core = "You are experiencing noticeable pressure."
    elif energy_level == 1:
        core = "Your energy level is low today."
    else:
        core = "Your condition is relatively stable."

    # 🧩 拼接（重点）
    extra_parts = []

    mood_text = format_phrase(mood_parts)
    event_text = format_phrase(event_parts)

    if mood_text:
        extra_parts.append(mood_text)
    if event_text:
        extra_parts.append(event_text)

    if extra_parts:
        extra = " You seem " + " ".join(extra_parts) + "."
    else:
        extra = ""

    return core + extra


def generate_tonight(energy_level, clean_mood):

    if energy_level == 1:
        return "Tonight, focus on rest. Do not push yourself."

    elif "Anxious" in clean_mood:
        return "Tonight, try to slow down and clear your mind."

    elif "Frustrated" in clean_mood:
        return "Step away from the source of frustration tonight."

    else:
        return "Take it easy tonight and keep things simple."


def generate_tomorrow(stress_level, clean_things):

    if stress_level == 4:
        return "Tomorrow, focus on one small step only."

    elif "Failed the exam again" in clean_things:
        return "Tomorrow, review calmly instead of rushing to fix everything."

    elif "Argued with someone" in clean_things:
        return "Tomorrow, consider resolving things calmly."

    else:
        return "You can move forward at your normal pace tomorrow."


if st.button("Generate"):
    if not clean_mood and not clean_things:
        st.error("Please select at least one mood or event.")

    else:
        summary = generate_summary(clean_mood, clean_things, stress_level, energy_level)
        tonight = generate_tonight(energy_level, clean_mood)
        tomorrow = generate_tomorrow(stress_level, clean_things)

        st.subheader("📝 Summary")
        st.info(summary)

        st.markdown("---")

        st.subheader("🌙 Tonight")
        st.success(tonight)

        st.markdown("---")

        st.subheader("🌅 Tomorrow")
        st.warning(tomorrow)
