
def classify_emotion_and_intent(text):
    text = text.lower()

    emotion_keywords = {
        "anxiety": ["anxious", "worried", "panic", "nervous"],
        "low_mood": ["sad", "depressed", "down", "hopeless", "upset"],
        "body_image": ["ugly", "fat", "hate my body", "unattractive"],
        "stress": ["stressed", "overwhelmed", "tired", "burnt out"],
        "confidence": ["confident", "strong", "capable"],
        "anger": ["angry", "frustrated", "irritated"]
    }

    intent_map = {
        "anxiety": "mood_reframe",
        "low_mood": "mood_reframe",
        "body_image": "body_acceptance",
        "stress": "stress_relief",
        "confidence": "confidence_boost",
        "anger": "mood_reframe"
    }

    for emotion, keywords in emotion_keywords.items():
        if any(word in text for word in keywords):
            return {"emotion": emotion, "intent": intent_map[emotion]}

    return {"emotion": "neutral", "intent": "neutral_support"}
