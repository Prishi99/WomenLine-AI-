import requests
import time
from speech_to_text import get_voice_input
from text_to_speech import speak_answer
from googletrans import Translator

# 🌐 Translator setup
translator = Translator()

# 🔍 Language detection
def detect_language(text):
    text = text.lower()
    if any(word in text for word in ["nahi", "kya", "mujhe", "kaise", "mere", "pati", "kyon", "kab", "kyu"]):
        return 'hi'
    else:
        return 'en'

# 🔁 Translate English answer to Hindi if needed
def translate_to_hinglish(text, lang):
    if lang == 'hi':
        try:
            translated = translator.translate(text, dest='hi').text
            return translated
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")
            return text
    return text

# 🔗 API request to backend
def get_bot_response(user_query):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/get_legal_answer",
            json={"query": user_query}
        )
        data = response.json()
        intent = data.get("intent", "Unknown")
        answer = data.get("answer", "Sorry, no answer found.")
        return intent, answer
    except Exception as e:
        return "error", f"Error contacting backend: {e}"

# 🎤 Voice or typed input
def get_user_input():
    print("💬 Type your question or press Enter to speak:")
    typed = input("> ").strip()
    return typed if typed else get_voice_input()

# 🧠 Main chatbot loop
def run_chatbot():
    print("🤖 Legal Voice Chatbot Ready!")
    speak_answer("Hello! How can I help you today?", lang='en')

    while True:
        user_query = get_user_input()
        if not user_query.strip():
            continue

        lang = detect_language(user_query)
        intent, bot_reply = get_bot_response(user_query)

        # 🔁 Translate if Hinglish
        translated_reply = translate_to_hinglish(bot_reply, lang)

        # 📋 Display
        print(f"📌 Predicted Intent: {intent}")
        print(f"🤖 Bot: {translated_reply}")
        speak_answer(translated_reply, lang=lang)

        time.sleep(1)
        follow_up = "Kya aap aur kuchh puchhna chahenge?" if lang == 'hi' else "Do you want to ask anything else?"
        speak_answer(follow_up, lang=lang)

        next_query = get_user_input().lower()
        if next_query in ['no', 'nahi', 'nahin', 'exit', 'quit', 'close']:
            goodbye = "Dhanyavaad! Aapka din shubh ho." if lang == 'hi' else "Thank you! Have a nice day."
            speak_answer(goodbye, lang=lang)
            break

# ▶️ Run
if __name__ == "__main__":
    run_chatbot()
