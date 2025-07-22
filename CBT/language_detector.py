import json
from langdetect import detect
import random

# ----------- Language Detection -----------
def detect_language(text):
    try:
        lang = detect(text)
        if lang in ['hi', 'ta', 'en']:
            return lang
        else:
            return 'en'
    except:
        return 'en'  # fallback

# ----------- Load Prompt File -----------
def load_prompts(file_path="cbt_prompts_all.json"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        return []

# ----------- Get Prompt in Detected Language -----------
def get_prompt(preferred_lang='en', intent=None, theme=None, cycle_phase=None):
    prompts = load_prompts()
    
    # Apply filters
    filtered = prompts
    if intent:
        filtered = [p for p in filtered if p['intent'] == intent]
    if theme:
        filtered = [p for p in filtered if p['theme'] == theme]
    if cycle_phase:
        filtered = [p for p in filtered if p['cycle_phase'] == cycle_phase]

    if not filtered:
        return "No matching prompt found. Please try a different category."

    selected_prompt = random.choice(filtered)
    
    # Pick correct language field or fallback to English
    lang_key = f"prompt_{preferred_lang}"
    if lang_key in selected_prompt and selected_prompt[lang_key].strip():
        return selected_prompt[lang_key]
    else:
        return selected_prompt["prompt_en"]

# ----------- Example usage -----------
if __name__ == "__main__":
    # Example user input
    user_input = "मुझे चिंता हो रही है"
    
    # Detect language
    lang_code = detect_language(user_input)
    print(f"Detected language: {lang_code}")
    
    # Get a prompt in that language
    prompt_text = get_prompt(preferred_lang=lang_code, intent="stress_relief", cycle_phase="menstruation")
    
    print(f"Prompt:\n{prompt_text}")
