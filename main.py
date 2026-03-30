import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error


def connect_database():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["MYSQLHOST"],
            user=st.secrets["MYSQLUSER"],
            password=st.secrets["MYSQLPASSWORD"],
            database=st.secrets["MYSQLDATABASE"],
            port=int(st.secrets["MYSQLPORT"])
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None


def save_to_database(user_name, clean_things, clean_mood, stress_level, energy_level, summary, tonight, tomorrow):
    conn = None
    cursor = None

    try:
        conn = connect_database()
        cursor = conn.cursor()

        query = """
        INSERT INTO mind_reset_records
        (user_name, things_happened, mood, stress_level, energy_level, summary, tonight, tomorrow)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            "user_name",
            ", ".join(clean_things),
            ", ".join(clean_mood),
            stress_level,
            energy_level,
            summary,
            tonight,
            tomorrow
        )

        cursor.execute(query, values)
        conn.commit()

    except Error as e:
        st.error(f"Database save failed: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def get_history(user_name):
    conn = None

    try:
        conn = connect_database()
        query = "SELECT * FROM mind_reset_records ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        return df

    except Error as e:
        st.error(f"Database load failed: {e}")
        return pd.DataFrame()

    finally:
        if conn is not None:
            conn.close()

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

div[data-testid="stForm"] {
    background-color: white;
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid #e9ecef;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🫀 Mind Reset System")
st.caption("A gentle check-in system for stressful or heavy days.")
st.info("Select your current mood, daily events, energy level, and stress level to receive a short reset note.")
st.markdown("---")

st.info("Enter your details below to generate your personalised AI health assessment.")
user_name = st.text_input("👤 Your name")

if not user_name:
    st.info("👆 Please enter your name to start the assessment.")
    st.stop()
st.markdown("---")

st.subheader("📝 Daily Check-In")
st.caption("Choose the options that best describe your current state.")

c1, c2 = st.columns(2)

with c1:
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

with c2:
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

st.caption("When you are ready, generate your reset note below.")
if st.button("✨ Generate Reset Note"):
    if not clean_mood and not clean_things:
        st.error("Please select at least one mood or event.")

    else:
        summary = generate_summary(clean_mood, clean_things, stress_level, energy_level)
        tonight = generate_tonight(energy_level, clean_mood)
        tomorrow = generate_tomorrow(stress_level, clean_things)

        save_to_database(user_name, clean_things, clean_mood, stress_level, energy_level, summary, tonight, tomorrow)

        st.subheader("🧾 Your Reset Note")
        st.caption("Here is a short emotional summary and a practical next step.")
        st.info(summary)

        st.markdown("---")

        st.subheader("🌙 Tonight")
        st.success(tonight)

        st.markdown("---")

        st.subheader("🌅 Tomorrow")
        st.warning(tomorrow)

    st.markdown("---")
    st.subheader("📜 History")
    st.caption("Your recent check-in records are shown below.")

    history_df = get_history()

    if not history_df.empty:
        st.dataframe(
            history_df[[
                "user_name",
                "created_at",
                "things_happened",
                "mood",
                "stress_level",
                "energy_level",
                "summary"
            ]],
            use_container_width=True
        )
    else:
        st.caption("No records yet.")

st.markdown("---")
st.caption("This tool is for reflection and general support only. It is not a medical or psychological diagnostic tool.")
