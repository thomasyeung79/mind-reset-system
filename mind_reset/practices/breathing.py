"""Check-in breathing category only. No practice bodies are packaged."""

def generate_breathing_practice(clean_mood, stress_level, energy_level, language):
    if 'Anxious' in clean_mood or stress_level >= 4:
        return {'type': 'calming'}
    elif 'Angry' in clean_mood:
        return {'type': 'pause'}
    elif energy_level <= 2 or 'Tired' in clean_mood:
        return {'type': 'recovery'}
    else:
        return {'type': 'basic'}
