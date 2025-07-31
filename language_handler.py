
import json
import re
from langdetect import detect

HINGLISH_HINTS = [
    'kyunki', 'samajh', 'mujhe', 'tum', 'hai', 'ho', 'kaise', 'kya',
    'mera', 'tera', 'raha', 'gaya', 'nahi', 'haan'
]

def is_hinglish(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(word in HINGLISH_HINTS for word in words) >= 2

def detect_language(text):
    try:
        if is_hinglish(text):
            return 'hinglish'
        lang = detect(text)
        return lang if lang in ['en', 'hi', 'ta', 'bn', 'mr'] else 'en'
    except:
        return 'en'

def load_prompts(file_path="cbt_prompts_period_health_dataset.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_prompt(preferred_lang='en', intent=None, theme=None, cycle_phase=None):
    prompts = load_prompts()

    def norm(s): return s.strip().lower() if s else ''
    best_score, best_prompt = -1, None

    for p in prompts:
        score = sum([
            norm(p.get('intent')) == norm(intent),
            norm(p.get('theme')) == norm(theme),
            norm(p.get('cycle_phase')) == norm(cycle_phase)
        ])
        if score > best_score:
            best_score = score
            best_prompt = p

    if not best_prompt:
        return "⚠️ No matching prompts available."

    lang_map = {
        'en': 'prompt',
        'hi': 'Hindi Translation',
        'ta': 'Tamil Translation',
        'bn': 'Bengali Translation',
        'mr': 'Marathi Translation',
        'hinglish': 'Hinglish Translation'
    }

    return best_prompt.get(lang_map.get(preferred_lang, 'prompt'), best_prompt.get('prompt', '⚠️ Prompt missing')).strip()
