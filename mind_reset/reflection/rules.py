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
