
from fastapi import FastAPI
from pydantic import BaseModel
from quiz_logic import detect_emotion_from_quiz
from nlp_emotion_detector import classify_emotion_and_intent
from language_handler import get_prompt, detect_language

app = FastAPI()

class QuizSubmission(BaseModel):
    answers: list
    phase: str

class TextInput(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    emotion: str
    language: str

@app.get("/")
def root():
    return {"message": "CBT backend is running!"}

@app.post("/submit_quiz")
def submit_quiz(data: QuizSubmission):
    emotion, category, phase = detect_emotion_from_quiz(data.answers, data.phase)
    prompt = get_prompt(intent=category, cycle_phase=phase, preferred_lang='en')
    return {
        "emotion": emotion,
        "category": category,
        "cycle_phase": phase,
        "prompt": prompt
    }

@app.post("/get_prompt_by_emotion")
def get_prompt_from_text(data: TextInput):
    result = classify_emotion_and_intent(data.text)
    lang = detect_language(data.text)
    prompt = get_prompt(intent=result['intent'], preferred_lang=lang)
    return {
        "detected_language": lang,
        "emotion": result['emotion'],
        "intent": result['intent'],
        "prompt": prompt
    }

@app.post("/get_translated_prompt")
def get_translated_prompt(data: TranslationRequest):
    prompt = get_prompt(intent=data.emotion, preferred_lang=data.language)
    return {
        "emotion": data.emotion,
        "language": data.language,
        "prompt": prompt
    }
if __name__ == "__main__":
    app.run("app:app", host="127.0.0.1", port=8000, reload=True)
