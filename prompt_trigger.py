from gtts import gTTS
import pygame
import json
import os
import time
from langdetect import detect
from difflib import SequenceMatcher

# Load multilingual datasets
datasets = {}
def load_datasets():
    files = {
        'hi': 'legal_qa_dataset_hi.json',
        'bn': 'legal_qa_dataset_bn.json',
        'mr': 'legal_qa_dataset_mr.json',
        'ta': 'legal_qa_dataset_ta.json'
    }
    for lang, file_name in files.items():
        with open(file_name, 'r', encoding='utf-8') as f:
            datasets[lang] = json.load(f)
load_datasets()

def trigger_prompt(query, intent):
    urgency_keywords = ['urgent', 'emergency', 'pain', 'bleeding', 'danger', 'hurt', 'दर्द', 'आपातकाल']
    if any(word in query.lower() for word in urgency_keywords):
        return "⚠️ This seems urgent. Do you need immediate help?"
    if intent == 'domestic_abuse':
        return "🛡️ Would you like help filing a complaint or seeking protection?"
    elif intent == 'workplace_harassment':
        return "📋 Do you want to understand your workplace rights or file a report?"
    elif intent == 'cyber_abuse':
        return "💻 Is this about online harassment, impersonation, or image misuse?"
    elif intent == 'emergency_medical':
        return "🚑 This may be a medical emergency. Please seek help immediately."
    else:
        return "ℹ️ Tell me more so I can help you better."

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(query, lang_code):
    best_match = None
    best_score = 0.0
    for item in datasets.get(lang_code, []):
        score = similarity(query, item['question'])
        if score > best_score:
            best_score = score
            best_match = item
    return best_match if best_score > 0.4 else None  # lowered threshold for better matching

def speak_text(text, lang='hi'):
    try:
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")

        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

    except PermissionError:
        print("⚠️ File access error: Please close or unlock response.mp3")

def run_voice_bot():
    print("🗣 Welcome to the Legal Voice Bot (Model-Free Version)")
    print("Type your query (or type 'exit' to quit):")
    while True:
        query = input("\nYour Query: ")
        if query.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        try:
            lang_code = detect(query)
        except:
            lang_code = 'hi'
        if lang_code not in datasets:
            lang_code = 'hi'

        best_match = find_best_match(query, lang_code)

        if best_match:
            intent = best_match['intent']
            answer = best_match['answer']
            prompt = trigger_prompt(query, intent)
        else:
            intent = None
            answer = {
                'hi': "माफ कीजिए, मुझे इसका उत्तर नहीं मिला।",
                'bn': "দুঃখিত, আমি এর উত্তর খুঁজে পাইনি।",
                'mr': "माफ करा, मला याचे उत्तर सापडले नाही.",
                'ta': "மன்னிக்கவும், இதற்கான பதிலை நான் கண்டுபிடிக்க முடியவில்லை."
            }.get(lang_code, "Sorry, I couldn't find an answer.")
            prompt = "ℹ️ I'm not sure I understood your query."

        print("🤖 Prompt:", prompt)
        print("📚 Answer:", answer)
        speak_text(answer, lang=lang_code)

if __name__ == "__main__":
    run_voice_bot()
