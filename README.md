# 🫀 Mind Reset System

A simple rule-based system for daily emotional check-ins and mental reset.

---

## 📌 Overview

The Mind Reset System is a lightweight application designed to help users:

- Reflect on their daily emotional state
- Identify stress and energy levels
- Receive structured and practical suggestions for tonight and tomorrow

This project focuses on transforming user inputs into natural, human-like feedback using rule-based logic.

---

## 🎯 Features

- Multi-select input for moods and daily events
- Structured stress and energy level assessment
- Intelligent summary generation based on combined inputs
- Personalised suggestions for:
  - 🌙 Tonight (short-term recovery)
  - 🌅 Tomorrow (next-step guidance)
- Clean and minimal UI using Streamlit

---

## 🧠 How It Works

The system uses a rule-based approach:

1. **Input Layer**
   - Mood (multi-select)
   - Daily events (multi-select)
   - Stress level (1–4)
   - Energy level (1–4)

2. **Processing Layer**
   - Combines emotional states and events
   - Evaluates stress and energy conditions
   - Applies conditional logic to generate responses

3. **Output Layer**
   - Summary (overall emotional state)
   - Tonight advice (immediate action)
   - Tomorrow advice (forward direction)

---

## 🧾 Example Output

**Input:**
- Mood: Tired, Anxious  
- Event: Had a long day  
- Stress: High  
- Energy: Low  

**Output:**

> You are under pressure and feeling drained.  
> You seem mentally tired and anxious after a long day.  

**Tonight:**  
Take it easy and allow yourself to rest.

**Tomorrow:**  
Focus on one clear task and avoid overload.

---

## 🛠 Tech Stack

- Python
- Streamlit

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run your_file_name.py
