import csv
import random
import re
from langdetect import detect

# ----------- Better Hinglish Detection -----------
HINGLISH_HINTS = [
    'nahi', 'ha', 'haan', 'kyun', 'achha', 'accha', 'kya', 'tum', 'kaise', 'hai', 'tha',
    'chal', 'mat', 'bhai', 'thik', 'theek', 'nhi', 'mera', 'tera', 'rha', 'raha', 'diya',
    'gaya', 'hota', 'karte', 'karna', 'bhi', 'lag', 'rha', 'h', 'or', 'se', 'mujhe',
    'chichidipan', 'main', 'apna', 'dil', 'bol', 'kyunki', 'samajh'
]

def is_hinglish(text):
    words = re.findall(r'\b\w+\b', text.lower())
    hindi_like = sum(word in HINGLISH_HINTS for word in words)
    return hindi_like >= 2

def detect_language(text):
    try:
        if is_hinglish(text):
            return 'hinglish'
        lang = detect(text)
        return lang if lang in ['hi', 'ta', 'bn', 'mr', 'en'] else 'en'
    except:
        return 'en'

# ----------- Load Prompt File from CSV -----------
def load_prompts(file_path="CBT_PROPMT - Sheet1.csv"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        return []

# ----------- Get Prompt in Detected Language -----------
def get_prompt(preferred_lang='en', intent=None, theme=None, cycle_phase=None):
    prompts = load_prompts()
    
    def norm(s):
        return s.strip().lower() if s else ''

    intent = norm(intent)
    theme = norm(theme)
    cycle_phase = norm(cycle_phase)

    best_score = -1
    best_prompt = None

    for p in prompts:
        score = 0
        if norm(p.get('intent')) == intent:
            score += 1
        if norm(p.get('theme')) == theme:
            score += 1
        if norm(p.get('cycle_phase')) == cycle_phase:
            score += 1

        if score > best_score:
            best_score = score
            best_prompt = p

    if not best_prompt:
        return "⚠️ Sorry, no prompts are available in the dataset."

    lang_map = {
        'en': 'prompt',
        'hi': 'Hindi Translation',
        'ta': 'Tamil Translation',
        'bn': 'Bengali Translation',
        'mr': 'Marathi Translation',
        'hinglish': 'Hinglish Translation'
    }

    lang_field = lang_map.get(preferred_lang, 'prompt')
    prompt_text = best_prompt.get(lang_field)

    if prompt_text and prompt_text.strip():
        return prompt_text.strip()
    else:
        return best_prompt.get('prompt', '⚠️ Prompt not available')
