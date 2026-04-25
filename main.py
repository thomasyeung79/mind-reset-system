import random
import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Mind Reset System",
    page_icon="✝️",
    layout="wide"
)

JSON_FILE = "insight_records.json"

def save_to_json(record):
    records = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                records = []

    records.append(record)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_history():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return pd.DataFrame(data)
            except json.JSONDecodeError:
                return pd.DataFrame()
    return pd.DataFrame()

TEXTS = {
    "English": {
        "title": "✝️ Insight to Action",
        "caption": "A faith-based reflection system for emotional reset and daily practice.",
        "info": "Select your current mood, daily events, energy level, and stress level to receive structured guidance.",
        "mode": "Select Mode",
        "topic_mode": "Topic Selection Mode",
        "auto": "Auto",
        "manual": "Manual",
        "daily_checkin": "📝 Daily Check-In",
        "daily_caption": "Choose the options that best describe your current state.",
        "reflection_topic": "✝️ Reflection Topic",
        "choose_topic": "Choose a reflection topic:",
        "things": "Current things",
        "mood": "Current mood",
        "energy": "Energy level:",
        "stress": "Stress level:",
        "button": "✨ Generate Reset Note",
        "error": "Please select at least one mood or event.",
        "reset_note": "🧾 Your Reset Note",
        "reset_caption": "Here is a short emotional summary and practical guidance.",
        "matched_topic": "Matched Topic",
        "insight": "🧠 Insight",
        "truth": "✝️ Truth",
        "scripture": "📖 Scripture",
        "practice": "🪜 Practice",
        "tonight": "🌙 Tonight",
        "tomorrow": "🌅 Tomorrow",
        "breathing": "🌬 Breathing Practice",
        "purpose": "Purpose",
        "steps": "Steps",
        "spiritual_guidance": "✝️ Spiritual Guidance",
        "reflection": "Reflection",
        "faith_action": "Faith Action",
        "story_title": "📖 Your Story Today",
        "disclaimer": "This tool is for reflection and general support only. It is not a medical, psychological, or theological authority."
    },
    "中文": {
        "title": "✝️ 从内在觉察到具体行动",
        "caption": "一个融合信仰与觉察的反思系统，帮助实现情绪重整与日常实践。",
        "info": "选择你当前的情绪、事件、能量和压力状态，获得结构化引导。",
        "mode": "选择模式",
        "topic_mode": "主题选择模式",
        "auto": "自动",
        "manual": "手动",
        "daily_checkin": "📝 今日状态记录",
        "daily_caption": "请选择最符合你当前状态的选项。",
        "reflection_topic": "✝️ 反思主题",
        "choose_topic": "选择一个反思主题：",
        "things": "当前发生的事情",
        "mood": "当前情绪",
        "energy": "能量水平：",
        "stress": "压力水平：",
        "button": "✨ 生成重整笔记",
        "error": "请至少选择一个情绪或事件。",
        "reset_note": "🧾 你的重整笔记",
        "reset_caption": "以下是你的状态总结与实践引导。",
        "matched_topic": "匹配主题",
        "insight": "🧠 觉察",
        "truth": "✝️ 原则",
        "scripture": "📖 经文",
        "practice": "🪜 实践",
        "tonight": "🌙 今晚",
        "tomorrow": "🌅 明天",
        "breathing": "🌬 呼吸练习",
        "purpose": "目的",
        "steps": "步骤",
        "spiritual_guidance": "✝️ 属灵引导",
        "reflection": "反思",
        "faith_action": "信仰行动",
        "story_title": "📖 你今天的故事",
        "disclaimer": "本工具仅用于个人反思与一般支持，不构成医学、心理或神学权威建议。"
    },
    "한국어": {
        "title": "✝️ 내면의 통찰에서 실제 행동으로",
        "caption": "신앙과 인식을 결합한 성찰 시스템으로, 감정의 회복과 일상의 실천을 돕습니다.",
        "info": "현재 기분, 하루의 사건, 에너지와 스트레스 수준을 선택하세요.",
        "mode": "모드 선택",
        "topic_mode": "주제 선택 모드",
        "auto": "자동",
        "manual": "수동",
        "daily_checkin": "📝 오늘의 체크인",
        "daily_caption": "현재 상태에 가장 가까운 항목을 선택하세요.",
        "reflection_topic": "✝️ 성찰 주제",
        "choose_topic": "성찰 주제를 선택하세요:",
        "things": "오늘 있었던 일",
        "mood": "현재 기분",
        "energy": "에너지 수준:",
        "stress": "스트레스 수준:",
        "button": "✨ 리셋 노트 생성",
        "error": "기분 또는 사건을 하나 이상 선택하세요.",
        "reset_note": "🧾 나의 리셋 노트",
        "reset_caption": "현재 상태 요약과 실천 안내입니다.",
        "matched_topic": "매칭된 주제",
        "insight": "🧠 통찰",
        "truth": "✝️ 원칙",
        "scripture": "📖 성경 구절",
        "practice": "🪜 실천",
        "tonight": "🌙 오늘 밤",
        "tomorrow": "🌅 내일",
        "breathing": "🌬 호흡 연습",
        "purpose": "목적",
        "steps": "단계",
        "spiritual_guidance": "✝️ 신앙적 안내",
        "reflection": "성찰",
        "faith_action": "신앙적 행동",
        "story_title": "📖 오늘의 이야기",
        "disclaimer": "이 도구는 개인 성찰과 일반적인 지원을 위한 것이며 의학적, 심리적, 신학적 권위가 아닙니다."
    }
}

MOOD_OPTIONS = {
    "Low": {"English": "Low", "中文": "低落", "한국어": "기분이 낮음"},
    "Tired": {"English": "Tired", "中文": "疲惫", "한국어": "피곤함"},
    "Anxious": {"English": "Anxious", "中文": "焦虑", "한국어": "불안함"},
    "Angry": {"English": "Angry", "中文": "生气", "한국어": "화남"},
    "Numb": {"English": "Numb", "中文": "麻木", "한국어": "무감각함"},
    "Calm": {"English": "Calm", "中文": "平静", "한국어": "평온함"},
}

EVENT_OPTIONS = {
    "Academic or work-related issue": {
        "English": "Academic or work-related issue",
        "中文": "学习或工作方面的困扰",
        "한국어": "학업 또는 업무 관련 문제"
    },
    "Had a long day": {
        "English": "Had a long day",
        "中文": "今天很漫长很累",
        "한국어": "긴 하루를 보냄"
    },
    "Argued with someone": {
        "English": "Argued with someone",
        "中文": "和别人发生争执",
        "한국어": "누군가와 다툼"
    },
    "Nothing special": {
        "English": "Nothing special",
        "中文": "没什么特别的事",
        "한국어": "특별한 일 없음"
    },
}

TOPIC_OPTIONS = {
    "Faith during pressure": {
        "English": "Faith during pressure",
        "中文": "压力中的信心",
        "한국어": "압박 속의 믿음"
    },
    "Patience before reaction": {
        "English": "Patience before reaction",
        "中文": "反应之前的忍耐",
        "한국어": "반응하기 전의 인내"
    },
    "Discipline and action": {
        "English": "Discipline and action",
        "中文": "自律与行动",
        "한국어": "훈련과 행동"
    },
    "Rest and renewal": {
        "English": "Rest and renewal",
        "中文": "休息与更新",
        "한국어": "쉼과 회복"
    },
    "Forgiveness and peace": {
        "English": "Forgiveness and peace",
        "中文": "宽恕与平安",
        "한국어": "용서와 평안"
    },
    "Gratitude and peace": {
        "English": "Gratitude and peace",
        "中文": "感恩与平安",
        "한국어": "감사와 평안"
    },
}

SCRIPTURE_DB = {
    "Philippians 4:6": {
        "English": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.",
        "中文": "在任何事上都不要忧虑；然而要在一切事上，藉着祷告和祈求，以感谢的心把你们所求的告诉神。",
        "한국어": "아무것도 염려하지 말고 모든 일에 기도와 간구로 여러분이 필요로 하는 것을 감사하는 마음으로 하나님께 말씀드리십시오."
    },
    "1 Peter 5:7": {
        "English": "Cast all your anxiety on him because he cares for you.",
        "中文": "你们要把一切忧虑都卸给神，因为他顾念你们。",
        "한국어": "여러분의 염려를 다 하나님께 맡기십시오. 하나님이 여러분을 보살피고 계십니다."
    },
    "Psalm 56:3": {
        "English": "When I am afraid, I put my trust in you.",
        "中文": "我害怕的时候，我要依靠你。",
        "한국어": "내가 두려울 때 주를 신뢰하겠습니다."
    },
    "Matthew 11:28": {
        "English": "Come to me, all you who are weary and burdened, and I will give you rest.",
        "中文": "所有劳苦和背负重担的人哪，到我这里来吧！我将使你们得到安息。",
        "한국어": "수고하고 무거운 짐 진 사람들아, 다 나에게 오너라. 내가 너희를 쉬게 하겠다."
    },
    "Isaiah 40:29": {
        "English": "He gives strength to the weary and increases the power of the weak.",
        "中文": "疲乏的，他赐力量；无力的，他加能力。",
        "한국어": "그는 피곤한 자에게 힘을 주시고 무능한 자에게 능력을 더하신다."
    },
    "Psalm 23:1": {
        "English": "The LORD is my shepherd, I lack nothing.",
        "中文": "耶和华是我的牧者，我必不缺乏。",
        "한국어": "여호와는 나의 목자시니 내가 부족함이 없으리라."
    },
    "Psalm 4:8": {
        "English": "In peace I will lie down and sleep, for you alone, LORD, make me dwell in safety.",
        "中文": "我必在平安中躺下并睡着；因为唯独你——耶和华啊，你使我安然居住！",
        "한국어": "내가 편안하게 누워 잘 수 있는 것은 주께서 나를 안전하게 지켜 주시기 때문입니다."
    },
    "James 1:19": {
        "English": "Everyone should be quick to listen, slow to speak and slow to become angry.",
        "中文": "每个人都该快快地听，不急于发言、不急于动怒。",
        "한국어": "누구든지 듣기는 속히 하고 말은 천천히 하며 함부로 성내지 마십시오."
    },
    "Proverbs 15:1": {
        "English": "A gentle answer turns away wrath, but a harsh word stirs up anger.",
        "中文": "温和的回答，使怒火消退；尖刻的话语，会激起怒气。",
        "한국어": "부드러운 대답은 분노를 가라앉혀도 과격한 말은 분노를 일으킨다."
    },
    "Matthew 5:9": {
        "English": "Blessed are the peacemakers, for they will be called children of God.",
        "中文": "使人和睦的人是蒙福的，因为他们将被称为神的儿女。",
        "한국어": "화평을 이루는 사람들은 행복하다. 그들은 하나님의 아들이라 불릴 것이다."
    },
    "Romans 12:18": {
        "English": "If it is possible, as far as it depends on you, live at peace with everyone.",
        "中文": "如果有可能，尽量在你们的事上与所有的人和睦。",
        "한국어": "가능한 한 최선을 다해 모든 사람과 사이좋게 지내십시오."
    },
    "Psalm 46:10": {
        "English": "Be still, and know that I am God.",
        "中文": "你们要休息，要知道我是神。",
        "한국어": "너희는 잠잠하라! 내가 하나님인 것을 알아라!"
    },
    "Psalm 145:18": {
        "English": "The LORD is near to all who call on him in truth.",
        "中文": "耶和华与所有真诚呼求他的人相近。",
        "한국어": "여호와께서는 진실한 마음으로 부르짖는 모든 자에게 가까이하신다."
    },
    "Colossians 3:15": {
        "English": "Let the peace of Christ rule in your hearts.",
        "中文": "又要让基督的和平在你们心里做主。",
        "한국어": "그리스도의 평안이 여러분의 마음을 다스리게 하십시오."
    },
    "Colossians 3:23": {
        "English": "Whatever you do, work at it with all your heart, as working for the Lord.",
        "中文": "你们无论做什么，都要从心里去做，像是为主做的。",
        "한국어": "무슨 일을 하든지 주님께 하듯 성실하게 하십시오."
    },
    "Galatians 6:9": {
        "English": "Let us not become weary in doing good.",
        "中文": "我们行美善的事不要丧胆。",
        "한국어": "선한 일을 하다가 낙심하지 맙시다."
    },
    "Proverbs 16:3": {
        "English": "Commit to the LORD whatever you do.",
        "中文": "当把你所做的交托给耶和华。",
        "한국어": "네가 하는 일을 여호와께 맡겨라."
    },
    "Colossians 3:13": {
        "English": "Forgive as the Lord forgave you.",
        "中文": "正如主饶恕了你们，你们也当如此。",
        "한국어": "주님께서 여러분을 용서하신 것같이 서로 용서하십시오."
    },
    "1 Thessalonians 5:18": {
        "English": "Give thanks in all circumstances.",
        "中文": "凡事感谢。",
        "한국어": "모든 일에 감사하십시오."
    },
    "Psalm 126:3": {
        "English": "The LORD has done great things for us, and we are filled with joy.",
        "中文": "耶和华为我们行了大事，我们就欢喜。",
        "한국어": "여호와께서 우리를 위해 큰 일을 행하셨으니 우리는 기쁨으로 가득하다."
    },
}

CHECKIN_TEXT = {
    "English": {
        "title": "📝 Check-in Panel",
        "caption": "Tell the system how you feel today."
    },
    "中文": {
        "title": "📝 状态记录",
        "caption": "记录你此刻的状态"
    },
    "한국어": {
        "title": "📝 상태 체크",
        "caption": "지금의 상태를 기록하세요"
    }
}

HISTORY_TEXT = {
    "English": {
        "title": "📜 History",
        "caption": "Your past reflections are saved below."
    },
    "中文": {
        "title": "📜 历史记录",
        "caption": "你过去的记录会显示在这里。"
    },
    "한국어": {
        "title": "📜 기록",
        "caption": "이전에 작성한 기록을 확인할 수 있습니다."
    }
}

st.markdown("""
<style>
.block-container {
    padding-top: 2.4rem;
    padding-bottom: 3rem;
    max-width: 1000px;
}

.hero {
    background: linear-gradient(135deg, #f8fbff, #eef4ff);
    padding: 2rem;
    border-radius: 30px;
    border: 1px solid #e5ebf5;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    margin-bottom: 1.4rem;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 850;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    color: #5f6b7a;
    font-size: 1rem;
    line-height: 1.65;
}

.app-card {
    background: #ffffff;
    padding: 1.3rem 1.5rem;
    border-radius: 24px;
    border: 1px solid #edf0f5;
    box-shadow: 0 6px 18px rgba(0,0,0,0.035);
    margin: 1rem 0;
}

.result-card {
    background: #ffffff;
    padding: 1.2rem 1.4rem;
    border-radius: 22px;
    border-left: 6px solid #1f6feb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.035);
    margin: 1rem 0;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 750;
    margin-bottom: 0.35rem;
}

.small-caption {
    color: #6c757d;
    font-size: 0.92rem;
}

div[data-testid="stAlert"] {
    border-radius: 16px;
}

.stButton > button {
    width: 100%;
    border-radius: 999px;
    padding: 0.75rem 1.4rem;
    font-weight: 800;
    border: none;
    background: #1f6feb;
    color: white;
}

.stButton > button:hover {
    background: #185abc;
    color: white;
}

hr {
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

def scripture_text(key, language):
    return f"{SCRIPTURE_DB[key][language]} — {key}"

def generate_summary(clean_mood, clean_things, stress_level, energy_level, language):
    if language == "中文":
        if stress_level == 4 and energy_level == 1:
            return "你现在可能感到压力很大，同时也非常疲惫。"
        elif stress_level >= 3 and energy_level <= 2:
            return "你现在处在一定压力之下，能量也偏低。"
        elif stress_level >= 3:
            return "你现在正在经历比较明显的压力。"
        elif energy_level == 1:
            return "你今天的能量比较低，需要温和地对待自己。"
        elif "Calm" in clean_mood:
            return "你今天整体比较平静，适合做一些感恩和整理。"
        else:
            return "你目前的状态整体比较稳定。"

    elif language == "한국어":
        if stress_level == 4 and energy_level == 1:
            return "현재 압박감이 크고 매우 지친 상태일 수 있습니다."
        elif stress_level >= 3 and energy_level <= 2:
            return "현재 스트레스를 받고 있으며 에너지도 낮은 편입니다."
        elif stress_level >= 3:
            return "현재 뚜렷한 압박감을 느끼고 있습니다."
        elif energy_level == 1:
            return "오늘은 에너지가 낮아 자신을 부드럽게 돌볼 필요가 있습니다."
        elif "Calm" in clean_mood:
            return "오늘은 비교적 평온한 상태이며 감사와 정리에 적합합니다."
        else:
            return "현재 상태는 전반적으로 안정적입니다."

    else:
        if stress_level == 4 and energy_level == 1:
            return "You may be feeling overwhelmed and exhausted."
        elif stress_level >= 3 and energy_level <= 2:
            return "You are under pressure and your energy is relatively low."
        elif stress_level >= 3:
            return "You are experiencing noticeable pressure."
        elif energy_level == 1:
            return "Your energy level is low today, so be gentle with yourself."
        elif "Calm" in clean_mood:
            return "You seem relatively calm today, which is a good moment for gratitude and reflection."
        else:
            return "Your current condition is relatively stable."


def generate_tonight(energy_level, clean_mood, language):
    if language == "中文":
        if energy_level == 1:
            return "今晚先专注休息，不要再强迫自己。"
        elif "Anxious" in clean_mood:
            return "今晚试着慢下来，把注意力带回呼吸。"
        elif "Angry" in clean_mood:
            return "今晚先离开让你烦躁的情境，不急着回应。"
        else:
            return "今晚让事情简单一点，温和地结束这一天。"

    elif language == "한국어":
        if energy_level == 1:
            return "오늘 밤은 휴식에 집중하고 자신을 밀어붙이지 마세요."
        elif "Anxious" in clean_mood:
            return "오늘 밤은 속도를 늦추고 호흡으로 주의를 돌려보세요."
        elif "Angry" in clean_mood:
            return "오늘 밤은 화나게 하는 상황에서 잠시 벗어나세요."
        else:
            return "오늘 밤은 단순하게 보내며 하루를 부드럽게 마무리하세요."

    else:
        if energy_level == 1:
            return "Tonight, focus on rest. Do not push yourself."
        elif "Anxious" in clean_mood:
            return "Tonight, try to slow down and return your attention to breathing."
        elif "Angry" in clean_mood:
            return "Step away from the source of frustration tonight."
        else:
            return "Take it easy tonight and keep things simple."


def generate_tomorrow(stress_level, clean_things, language):
    if language == "中文":
        if stress_level == 4:
            return "明天只专注一个小步骤，不需要一次解决所有问题。"
        elif "Failed the exam again" in clean_things:
            return "明天可以冷静复盘，而不是急着证明自己。"
        elif "Argued with someone" in clean_things:
            return "明天可以考虑用更平和的方式处理关系。"
        else:
            return "明天可以按照正常节奏继续前进。"

    elif language == "한국어":
        if stress_level == 4:
            return "내일은 한 가지 작은 단계에만 집중하세요."
        elif "Failed the exam again" in clean_things:
            return "내일은 서두르지 말고 차분히 복습해 보세요."
        elif "Argued with someone" in clean_things:
            return "내일은 더 평화로운 방식으로 관계를 정리해 보세요."
        else:
            return "내일은 평소의 속도로 다시 앞으로 나아가도 됩니다."

    else:
        if stress_level == 4:
            return "Tomorrow, focus on one small step only."
        elif "Failed the exam again" in clean_things:
            return "Tomorrow, review calmly instead of rushing to fix everything."
        elif "Argued with someone" in clean_things:
            return "Tomorrow, consider resolving things calmly."
        else:
            return "You can move forward at your normal pace tomorrow."


def auto_select_topic(clean_mood, clean_things, stress_level, energy_level):
    if "Anxious" in clean_mood or stress_level >= 4:
        return "Faith during pressure"
    elif "Angry" in clean_mood or "Argued with someone" in clean_things:
        return "Patience before reaction"
    elif "Tired" in clean_mood or energy_level <= 2:
        return "Rest and renewal"
    elif "Academic or work-related issue" in clean_things:
        return "Discipline and action"
    elif "Calm" in clean_mood and stress_level <= 2:
        return "Gratitude and peace"
    else:
        return "Discipline and action"


def generate_topic_guidance(topic, language):
    topic_guides = {
        "Faith during pressure": {
            "principle": {
                "English": "Faith is practiced when pressure is present, not when life is easy.",
                "中文": "信心不是在轻松时才实践，而是在压力中被操练。",
                "한국어": "믿음은 삶이 쉬울 때가 아니라 압박 속에서 실천됩니다."
            },
            "scriptures": ["Philippians 4:6", "1 Peter 5:7", "Psalm 56:3"],
            "practice": {
                "English": [
                    "Name one worry and pray about it.",
                    "Write down what is stressing you and release it.",
                    "Take one small step instead of trying to solve everything."
                ],
                "中文": [
                    "写下一个让你忧虑的事情，并为它祷告。",
                    "写下正在压迫你的事情，然后尝试把它交托出去。",
                    "不要试图一次解决所有问题，先迈出一个小步骤。"
                ],
                "한국어": [
                    "걱정되는 한 가지를 적고 그것을 위해 기도하세요.",
                    "당신을 압박하는 일을 적고 내려놓아 보세요.",
                    "모든 것을 한 번에 해결하려 하지 말고 작은 한 걸음을 시작하세요."
                ]
            }
        },
        "Patience before reaction": {
            "principle": {
                "English": "Patience creates space between emotion and response.",
                "中文": "忍耐是在情绪和回应之间创造空间。",
                "한국어": "인내는 감정과 반응 사이에 공간을 만듭니다."
            },
            "scriptures": ["James 1:19", "Proverbs 15:1", "Matthew 5:9"],
            "practice": {
                "English": [
                    "Pause before responding.",
                    "Take one breath before speaking.",
                    "Choose calm over reaction."
                ],
                "中文": [
                    "回应之前先暂停一下。",
                    "说话前先深呼吸一次。",
                    "选择平静，而不是立刻反应。"
                ],
                "한국어": [
                    "반응하기 전에 잠시 멈추세요.",
                    "말하기 전에 한 번 숨을 쉬세요.",
                    "즉각적인 반응보다 평온함을 선택하세요."
                ]
            }
        },
        "Discipline and action": {
            "principle": {
                "English": "Growth comes from small faithful actions, not sudden motivation.",
                "中文": "成长来自持续的小行动，而不是突然的动力。",
                "한국어": "성장은 갑작스러운 동기보다 작은 충실한 행동에서 옵니다."
            },
            "scriptures": ["Colossians 3:23", "Galatians 6:9", "Proverbs 16:3"],
            "practice": {
                "English": [
                    "Choose one task and work on it for ten minutes.",
                    "Start with one small action instead of waiting for motivation.",
                    "Write down one thing you can complete today."
                ],
                "中文": [
                    "选择一件事，先做十分钟。",
                    "不要等待动力，先开始一个小行动。",
                    "写下今天可以完成的一件小事。"
                ],
                "한국어": [
                    "한 가지 일을 선택해 10분 동안 해보세요.",
                    "동기를 기다리지 말고 작은 행동부터 시작하세요.",
                    "오늘 끝낼 수 있는 한 가지를 적어보세요."
                ]
            }
        },
        "Rest and renewal": {
            "principle": {
                "English": "Rest is not weakness; it is part of renewal.",
                "中文": "休息不是软弱，而是更新的一部分。",
                "한국어": "쉼은 약함이 아니라 회복의 일부입니다."
            },
            "scriptures": ["Matthew 11:28", "Isaiah 40:29", "Psalm 4:8"],
            "practice": {
                "English": [
                    "Stop one unnecessary task tonight and allow yourself to recover.",
                    "Take a short rest without blaming yourself.",
                    "Put your phone away for ten minutes and let your mind slow down."
                ],
                "中文": [
                    "今晚停下一件不必要的事，让自己恢复。",
                    "短暂休息一下，不要责备自己。",
                    "把手机放下十分钟，让心慢下来。"
                ],
                "한국어": [
                    "오늘 밤 불필요한 일을 하나 멈추고 회복하세요.",
                    "자책하지 말고 잠시 쉬세요.",
                    "휴대폰을 10분 내려놓고 마음을 천천히 가라앉히세요."
                ]
            }
        },
        "Forgiveness and peace": {
            "principle": {
                "English": "Forgiveness does not deny pain, but it releases your heart from being controlled by it.",
                "中文": "宽恕不是否认伤痛，而是不再让伤痛控制你的心。",
                "한국어": "용서는 아픔을 부정하는 것이 아니라 그 아픔에 마음이 지배되지 않게 하는 것입니다."
            },
            "scriptures": ["Colossians 3:13", "Matthew 5:9", "Romans 12:18"],
            "practice": {
                "English": [
                    "Write down what hurt you, then write one sentence of release.",
                    "Pray for peace before you decide what to say.",
                    "Choose one peaceful response instead of replaying the conflict."
                ],
                "中文": [
                    "写下让你受伤的事，再写一句释放自己的话。",
                    "在决定说什么之前，先为平安祷告。",
                    "选择一个和平的回应，而不是反复回放冲突。"
                ],
                "한국어": [
                    "상처받은 일을 적고, 내려놓는 한 문장을 적어보세요.",
                    "무엇을 말할지 결정하기 전에 평안을 위해 기도하세요.",
                    "갈등을 반복해서 떠올리기보다 평화로운 반응을 선택하세요."
                ]
            }
        },
        "Gratitude and peace": {
            "principle": {
                "English": "Peace is not only the absence of trouble, but the awareness of grace.",
                "中文": "平安不只是没有问题，而是能觉察恩典的存在。",
                "한국어": "평안은 문제가 없는 상태만이 아니라 은혜를 알아차리는 마음입니다."
            },
            "scriptures": ["1 Thessalonians 5:18", "Colossians 3:15", "Psalm 126:3"],
            "practice": {
                "English": [
                    "Write down three things you are thankful for today.",
                    "Pause and notice one small gift in this moment.",
                    "Share one kind word with someone today."
                ],
                "中文": [
                    "写下今天三件值得感恩的事。",
                    "暂停一下，觉察此刻一个小小的恩典。",
                    "今天对一个人说一句温和的话。"
                ],
                "한국어": [
                    "오늘 감사한 세 가지를 적어보세요.",
                    "잠시 멈추고 지금 이 순간의 작은 선물을 알아차리세요.",
                    "오늘 누군가에게 따뜻한 말 한마디를 전하세요."
                ]
            }
        },
    }

    data = topic_guides[topic]
    verse_key = random.choice(data["scriptures"])

    return {
        "principle": data["principle"][language],
        "scripture": scripture_text(verse_key, language),
        "practice": random.choice(data["practice"][language])
    }


def generate_breathing_practice(clean_mood, stress_level, energy_level, language):
    if "Anxious" in clean_mood or stress_level >= 4:
        return {
            "title": {"English": "Calming Breath", "中文": "安定呼吸", "한국어": "진정 호흡"}[language],
            "purpose": {
                "English": "Reduce anxiety and return to the present moment.",
                "中文": "减轻焦虑，把注意力带回当下。",
                "한국어": "불안을 낮추고 현재 순간으로 돌아옵니다."
            }[language],
            "steps": {
                "English": [
                    "Find a quiet place and sit comfortably.",
                    "Relax your shoulders and keep your body still.",
                    "Inhale slowly through your nose.",
                    "Exhale slowly and gently.",
                    "When your mind wanders, gently bring it back to your breath.",
                    "Continue for 3–5 minutes."
                ],
                "中文": [
                    "找一个安静的地方，舒服地坐下。",
                    "放松肩膀，让身体稳定下来。",
                    "通过鼻子慢慢吸气。",
                    "缓慢而温和地呼气。",
                    "当念头跑开时，轻轻把注意力带回呼吸。",
                    "持续练习3到5分钟。"
                ],
                "한국어": [
                    "조용한 곳을 찾아 편안하게 앉으세요.",
                    "어깨를 이완하고 몸을 안정시키세요.",
                    "코로 천천히 숨을 들이마시세요.",
                    "천천히 부드럽게 숨을 내쉬세요.",
                    "생각이 흩어지면 부드럽게 호흡으로 돌아오세요.",
                    "3~5분 동안 계속하세요."
                ]
            }[language],
            "type": "calming"
        }

    elif "Angry" in clean_mood:
        return {
            "title": {"English": "Pause Breath", "中文": "暂停呼吸", "한국어": "멈춤 호흡"}[language],
            "purpose": {
                "English": "Create space between emotion and reaction.",
                "中文": "在情绪和反应之间创造空间。",
                "한국어": "감정과 반응 사이에 공간을 만듭니다."
            }[language],
            "steps": {
                "English": [
                    "Pause before reacting.",
                    "Take a slow inhale.",
                    "Take a longer exhale.",
                    "Notice tension in your body.",
                    "Repeat for 5 breaths.",
                    "Choose a response that brings peace."
                ],
                "中文": [
                    "在反应之前先暂停。",
                    "慢慢吸一口气。",
                    "更长地呼出这一口气。",
                    "觉察身体里的紧张。",
                    "重复5次呼吸。",
                    "选择一个能带来平安的回应。"
                ],
                "한국어": [
                    "반응하기 전에 잠시 멈추세요.",
                    "천천히 숨을 들이마시세요.",
                    "더 길게 숨을 내쉬세요.",
                    "몸의 긴장을 알아차리세요.",
                    "5번 반복하세요.",
                    "평화를 가져오는 반응을 선택하세요."
                ]
            }[language],
            "type": "pause"
        }

    elif energy_level <= 2 or "Tired" in clean_mood:
        return {
            "title": {"English": "Recovery Breath", "中文": "恢复呼吸", "한국어": "회복 호흡"}[language],
            "purpose": {
                "English": "Restore energy without forcing the body.",
                "中文": "不强迫身体，在温和中恢复能量。",
                "한국어": "몸을 억지로 밀어붙이지 않고 에너지를 회복합니다."
            }[language],
            "steps": {
                "English": [
                    "Sit or lie down comfortably.",
                    "Place one hand on your abdomen.",
                    "Breathe naturally at first.",
                    "Slowly deepen your breathing if comfortable.",
                    "Relax your body with each exhale.",
                    "Stop if you feel uncomfortable."
                ],
                "中文": [
                    "舒服地坐下或躺下。",
                    "把一只手放在腹部。",
                    "先自然呼吸。",
                    "如果感觉舒服，再慢慢加深呼吸。",
                    "每次呼气时让身体放松。",
                    "如果不舒服，就停止练习。"
                ],
                "한국어": [
                    "편안하게 앉거나 누우세요.",
                    "한 손을 복부 위에 올리세요.",
                    "먼저 자연스럽게 호흡하세요.",
                    "편안하다면 천천히 호흡을 깊게 하세요.",
                    "숨을 내쉴 때마다 몸을 이완하세요.",
                    "불편하면 멈추세요."
                ]
            }[language],
            "type": "recovery"
        }

    else:
        return {
            "title": {"English": "Mindful Breathing", "中文": "正念呼吸", "한국어": "마음챙김 호흡"}[language],
            "purpose": {
                "English": "Build awareness through simple breathing.",
                "中文": "通过简单呼吸培养觉察。",
                "한국어": "간단한 호흡을 통해 알아차림을 기릅니다."
            }[language],
            "steps": {
                "English": [
                    "Sit still in a quiet place.",
                    "Notice your natural breathing.",
                    "Follow each inhale.",
                    "Follow each exhale.",
                    "Gently return when distracted.",
                    "Practice for 3 minutes."
                ],
                "中文": [
                    "在安静的地方坐稳。",
                    "觉察自然呼吸。",
                    "跟随每一次吸气。",
                    "跟随每一次呼气。",
                    "分心时轻轻回到呼吸。",
                    "练习3分钟。"
                ],
                "한국어": [
                    "조용한 곳에 가만히 앉으세요.",
                    "자연스러운 호흡을 알아차리세요.",
                    "들이마심을 따라가세요.",
                    "내쉼을 따라가세요.",
                    "산만해지면 부드럽게 돌아오세요.",
                    "3분 동안 연습하세요."
                ]
            }[language],
            "type": "basic"
        }


def generate_spiritual_breathing(breathing_type, language):
    scripture_map = {
        "calming": ["Philippians 4:6", "1 Peter 5:7", "Psalm 56:3"],
        "recovery": ["Matthew 11:28", "Isaiah 40:29", "Psalm 23:1", "Psalm 4:8"],
        "pause": ["James 1:19", "Proverbs 15:1", "Matthew 5:9"],
        "basic": ["Psalm 46:10", "Psalm 145:18", "Colossians 3:15"],
    }

    reflection_map = {
        "calming": {
            "English": ["Trust grows when you release control.", "Fear becomes lighter when you are not carrying it alone."],
            "中文": ["当你放下控制，信靠就开始增长。", "当你不再独自背负恐惧，恐惧会变轻。"],
            "한국어": ["통제를 내려놓을 때 신뢰가 자랍니다.", "혼자 두려움을 짊어지지 않을 때 두려움은 가벼워집니다."]
        },
        "recovery": {
            "English": ["Rest is part of healing, not weakness.", "You are supported even when you feel empty."],
            "中文": ["休息是恢复的一部分，不是软弱。", "即使你感到空乏，你仍然被扶持。"],
            "한국어": ["쉼은 약함이 아니라 치유의 일부입니다.", "비어 있다고 느껴도 당신은 지지받고 있습니다."]
        },
        "pause": {
            "English": ["Wisdom grows in the space between feeling and reaction.", "Peace begins when you choose not to react immediately."],
            "中文": ["智慧存在于情绪与反应之间的那一刻。", "当你选择不立刻反应时，平静就开始了。"],
            "한국어": ["지혜는 감정과 반응 사이에서 자랍니다.", "즉각 반응하지 않을 때 평화가 시작됩니다."]
        },
        "basic": {
            "English": ["Stillness allows you to reconnect with awareness and faith.", "Quiet moments create deeper clarity."],
            "中文": ["安静让你重新连接觉察与信心。", "安静的时刻带来更深的清晰。"],
            "한국어": ["고요함은 인식과 믿음을 다시 연결해 줍니다.", "조용한 순간은 더 깊은 깨달음을 줍니다."]
        },
    }

    action_map = {
        "calming": {
            "English": ["Release one worry with each exhale.", "Breathe out slowly and surrender what you cannot control."],
            "中文": ["每一次呼气时，放下一个忧虑。", "慢慢呼气，把你无法控制的交托出去。"],
            "한국어": ["숨을 내쉴 때마다 걱정 하나를 내려놓으세요.", "천천히 내쉬며 통제할 수 없는 것을 맡기세요."]
        },
        "recovery": {
            "English": ["Allow yourself to slow down without guilt.", "Let your body relax with every exhale."],
            "中文": ["允许自己慢下来，不必内疚。", "每次呼气时，让身体放松一点。"],
            "한국어": ["죄책감 없이 천천히 쉬어도 괜찮습니다.", "숨을 내쉴 때마다 몸을 이완하세요."]
        },
        "pause": {
            "English": ["Pause, breathe, and choose peace over impulse.", "Take one deep breath before speaking."],
            "中文": ["暂停，呼吸，选择平静而不是冲动。", "说话前先深呼吸一次。"],
            "한국어": ["잠시 멈추고 숨 쉬며 충동 대신 평화를 선택하세요.", "말하기 전에 깊게 한 번 숨 쉬세요."]
        },
        "basic": {
            "English": ["Stay present and let your mind rest in God.", "Focus on your breath and let thoughts pass."],
            "中文": ["活在当下，让心在神里面安息。", "专注呼吸，让念头自然流过。"],
            "한국어": ["현재에 머물며 마음을 하나님 안에서 쉬게 하세요.", "호흡에 집중하고 생각을 흘려보내세요."]
        },
    }

    verse_key = random.choice(scripture_map[breathing_type])

    return {
        "scripture": scripture_text(verse_key, language),
        "reflection": random.choice(reflection_map[breathing_type][language]),
        "faith_action": random.choice(action_map[breathing_type][language])
    }


def generate_story(summary, tonight, tomorrow, spiritual, breathing, spiritual_breathing, language):
    if language == "中文":
        return f"""
今天你的状态可以这样理解：

**{summary}**

今晚，你可以先从一个简单的行动开始：

**{tonight}**

明天，不需要一次解决所有事情：

**{tomorrow}**

今天可以抓住的原则是：

**{spiritual["principle"]}**

可以默想的经文：

**{spiritual["scripture"]}**

一个实践步骤：

**{spiritual["practice"]}**

呼吸练习：

**{breathing["title"]}** — {breathing["purpose"]}

信仰行动：

**{spiritual_breathing["faith_action"]}**
"""

    elif language == "한국어":
        return f"""
오늘 당신의 상태는 이렇게 이해할 수 있습니다:

**{summary}**

오늘 밤은 작은 한 걸음부터 시작해 보세요:

**{tonight}**

내일 모든 것을 한 번에 해결할 필요는 없습니다:

**{tomorrow}**

오늘 붙들 수 있는 원칙은 다음과 같습니다:

**{spiritual["principle"]}**

묵상할 성경 구절:

**{spiritual["scripture"]}**

실천 단계:

**{spiritual["practice"]}**

호흡 연습:

**{breathing["title"]}** — {breathing["purpose"]}

신앙적 행동:

**{spiritual_breathing["faith_action"]}**
"""

    else:
        return f"""
Today, your current state can be described as:

**{summary}**

Tonight, you can begin with one simple step:

**{tonight}**

Tomorrow does not need to solve everything at once:

**{tomorrow}**

A principle to hold onto today:

**{spiritual["principle"]}**

Scripture for reflection:

**{spiritual["scripture"]}**

A practical step:

**{spiritual["practice"]}**

Breathing practice:

**{breathing["title"]}** — {breathing["purpose"]}

Faith action:

**{spiritual_breathing["faith_action"]}**
"""

language = st.selectbox("Language / 语言 / 언어", ["English", "中文", "한국어"])
t = TEXTS[language]

st.markdown(f"""
<div class="hero">
    <div class="hero-title">{t["title"]}</div>
    <div class="hero-subtitle">{t["caption"]}</div>
    <br>
    <div class="hero-subtitle">{t["info"]}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

ct = CHECKIN_TEXT[language]

st.markdown(f"""
<div class="app-card">
    <div class="section-title">{ct["title"]}</div>
    <div class="small-caption">{ct["caption"]}</div>
</div>
""", unsafe_allow_html=True)

mode = st.radio(
    t["mode"],
    ["Dashboard", "Story Mode"],
    horizontal=True
)

st.markdown("---")

st.subheader(t["daily_checkin"])
st.caption(t["daily_caption"])

username = st.text_input(
    "Username / 用户名 / 사용자 이름",
    placeholder="Enter your name"
)

st.markdown("---")

st.subheader(t["reflection_topic"])

topic_mode = st.radio(
    t["topic_mode"],
    ["Auto", "Manual"],
    format_func=lambda x: t["auto"] if x == "Auto" else t["manual"],
    horizontal=True
)

if topic_mode == "Manual":
    manual_topic = st.selectbox(
        t["choose_topic"],
        options=list(TOPIC_OPTIONS.keys()),
        format_func=lambda x: TOPIC_OPTIONS[x][language]
    )
else:
    manual_topic = None
    st.caption("Auto mode will match a topic based on your current state.")

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    clean_things = st.multiselect(
        t["things"],
        options=list(EVENT_OPTIONS.keys()),
        format_func=lambda x: EVENT_OPTIONS[x][language]
    )

    st.markdown("---")

    clean_mood = st.multiselect(
        t["mood"],
        options=list(MOOD_OPTIONS.keys()),
        format_func=lambda x: MOOD_OPTIONS[x][language]
    )

with c2:
    energy_level = st.selectbox(
        t["energy"],
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 - Exhausted" if language == "English" else ("1 - 精疲力尽" if language == "中文" else "1 - 매우 지침"),
            2: "2 - Normal" if language == "English" else ("2 - 普通" if language == "中文" else "2 - 보통"),
            3: "3 - Good" if language == "English" else ("3 - 良好" if language == "中文" else "3 - 좋음"),
            4: "4 - Very energetic" if language == "English" else ("4 - 很有活力" if language == "中文" else "4 - 매우 활기참"),
        }[x]
    )

    st.markdown("---")

    stress_level = st.selectbox(
        t["stress"],
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "1 - Relaxed" if language == "English" else ("1 - 放松" if language == "中文" else "1 - 편안함"),
            2: "2 - Manageable" if language == "English" else ("2 - 可控" if language == "中文" else "2 - 감당 가능"),
            3: "3 - High pressure" if language == "English" else ("3 - 压力较大" if language == "中文" else "3 - 높은 압박"),
            4: "4 - Overwhelmed" if language == "English" else ("4 - 不堪重负" if language == "中文" else "4 - 압도됨"),
        }[x]
    )

st.markdown("---")

if st.button(t["button"]):
    if not username:
        st.error("Please enter a username.")
    elif not clean_mood and not clean_things:
        st.error(t["error"])
    else:
        summary = generate_summary(clean_mood, clean_things, stress_level, energy_level, language)
        tonight = generate_tonight(energy_level, clean_mood, language)
        tomorrow = generate_tomorrow(stress_level, clean_things, language)

        if topic_mode == "Auto":
            topic = auto_select_topic(clean_mood, clean_things, stress_level, energy_level)
        else:
            topic = manual_topic

        spiritual = generate_topic_guidance(topic, language)
        breathing = generate_breathing_practice(clean_mood, stress_level, energy_level, language)
        spiritual_breathing = generate_spiritual_breathing(breathing["type"], language)

        record = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "language": language,
            "mode": mode,
            "topic_mode": topic_mode,
            "matched_topic": topic,
            "mood": clean_mood,
            "events": clean_things,
            "stress_level": stress_level,
            "energy_level": energy_level,
            "summary": summary,
            "tonight": tonight,
            "tomorrow": tomorrow,
            "principle": spiritual["principle"],
            "scripture": spiritual["scripture"],
            "practice": spiritual["practice"],
            "breathing_title": breathing["title"],
            "breathing_purpose": breathing["purpose"],
            "spiritual_scripture": spiritual_breathing["scripture"],
            "spiritual_reflection": spiritual_breathing["reflection"],
            "faith_action": spiritual_breathing["faith_action"]
        }

        storage_used = save_to_json(record)
        st.success(f"Record saved via {storage_used}.")

        story = generate_story(
            summary,
            tonight,
            tomorrow,
            spiritual,
            breathing,
            spiritual_breathing,
            language
        )

        if mode == "Dashboard":
            st.markdown(f"""
            <div class="result-card">
                <div class="section-title">{t["reset_note"]}</div>
                <div class="small-caption">{t["reset_caption"]}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### " + t["insight"])
            st.info(summary)

            st.markdown("---")
            st.caption(f"{t['matched_topic']}: {TOPIC_OPTIONS[topic][language]}")

            st.markdown("### " + t["truth"])
            st.success(spiritual["principle"])

            st.markdown("### " + t["scripture"])
            st.info(spiritual["scripture"])

            st.markdown("### " + t["practice"])
            st.warning(spiritual["practice"])

            st.markdown("---")

            st.markdown("### " + t["tonight"])
            st.success(tonight)

            st.markdown("### " + t["tomorrow"])
            st.warning(tomorrow)

            st.markdown("---")

            st.markdown("### " + t["breathing"])
            st.success(breathing["title"])

            st.markdown("**" + t["purpose"] + "**")
            st.info(breathing["purpose"])

            st.markdown("**" + t["steps"] + "**")
            for step in breathing["steps"]:
                st.write(f"- {step}")

            st.markdown("---")

            st.markdown("### " + t["spiritual_guidance"])

            st.markdown("**" + t["scripture"] + "**")
            st.info(spiritual_breathing["scripture"])

            st.markdown("**" + t["reflection"] + "**")
            st.write(spiritual_breathing["reflection"])

            st.markdown("**" + t["faith_action"] + "**")
            st.success(spiritual_breathing["faith_action"])

        elif mode == "Story Mode":
            st.subheader(t["story_title"])
            st.caption(f"{t['matched_topic']}: {TOPIC_OPTIONS[topic][language]}")
            st.markdown(story)

st.markdown("---")

ht = HISTORY_TEXT[language]

st.markdown(f"""
<div class="app-card">
    <div class="section-title">{ht["title"]}</div>
    <div class="small-caption">{ht["caption"]}</div>
</div>
""", unsafe_allow_html=True)

history_df = load_history()

if username:
    if not history_df.empty and "username" in history_df.columns:
        history_df = history_df[history_df["username"] == username]
    else:
        history_df = pd.DataFrame()
else:
    history_df = pd.DataFrame()

if not history_df.empty:
    history_df = history_df.iloc[::-1]

    for i, row in history_df.iterrows():
        record_time = row.get("created_at", "No time")
        record_summary = str(row.get("summary", "No summary"))
        record_topic = str(row.get("matched_topic", "N/A"))

        with st.expander(f"{record_time} | {record_topic} | {record_summary[:35]}..."):
            st.markdown("### " + t["insight"])
            st.info(row.get("summary", ""))

            st.markdown("### " + t["truth"])
            st.success(row.get("principle", ""))

            st.markdown("### " + t["scripture"])
            st.info(row.get("scripture", ""))

            st.markdown("### " + t["practice"])
            st.warning(row.get("practice", ""))

            st.markdown("---")

            st.markdown("### " + t["tonight"])
            st.success(row.get("tonight", ""))

            st.markdown("### " + t["tomorrow"])
            st.warning(row.get("tomorrow", ""))

            st.markdown("---")

            st.markdown("### " + t["breathing"])
            st.success(row.get("breathing_title", ""))

            st.markdown("**" + t["purpose"] + "**")
            st.info(row.get("breathing_purpose", ""))

            st.markdown("### " + t["spiritual_guidance"])

            st.markdown("**" + t["scripture"] + "**")
            st.info(row.get("spiritual_scripture", ""))

            st.markdown("**" + t["reflection"] + "**")
            st.write(row.get("spiritual_reflection", ""))

            st.markdown("**" + t["faith_action"] + "**")
            st.success(row.get("faith_action", ""))

else:
    if username:
        st.caption("No records yet.")
    else:
        st.caption("Enter a username to view your history.")

st.markdown("---")
st.caption(t["disclaimer"])
