import json

def detect_emotion_from_quiz(answers, phase):
    score_map = [
        {"Energetic": 2, "Tired": -1, "Anxious": -2},
        {"Happy": 2, "Okay": 0, "Low": -2},
        {"Confident": 2, "Neutral": 0, "Insecure": -2},
        {"Not at all": 2, "A little": -1, "Very much": -2}
    ]
    score = sum(score_map[i].get(ans, 0) for i, ans in enumerate(answers))

    emotion_mapping = {
        "very_negative": (-10, -5),
        "low_mood": (-4, -1),
        "neutral": (0,),
        "positive": (1, 4),
        "very_positive": (5, 10)
    }

    category_mapping = {
        "very_negative": "stress_relief",
        "low_mood": "mood_reframe",
        "neutral": "neutral_support",
        "positive": "body_acceptance",
        "very_positive": "confidence_boost"
    }

    detected_emotion = "neutral"
    for emotion, score_range in emotion_mapping.items():
        if isinstance(score_range, tuple) and score_range[0] <= score <= score_range[1]:
            detected_emotion = emotion
            break
        elif score in score_range:
            detected_emotion = emotion
            break

    prompt_category = category_mapping[detected_emotion]
    return detected_emotion, prompt_category, phase
