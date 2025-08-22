# womenweek2task.py

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

# -------------------- Load dataset --------------------
CSV_FILE = "cbt_prompts_period_health_dataset.csv"

if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"Dataset file '{CSV_FILE}' not found in {os.getcwd()}")

df = pd.read_csv(CSV_FILE)

# -------------------- FastAPI app --------------------
app = FastAPI(title="WomenLine AI - Week 2 Emotion Detection API")

# -------------------- Request body model --------------------
class EmotionQuizRequest(BaseModel):
    answers: dict  # {"Q1": "Energetic", "Q2": "Low", ...}
    cycle_phase: str  # "pre-period", "menstruation", "post-period"

# -------------------- Scoring system --------------------
emotion_mapping = {
    "very_negative": (-10, -5),
    "low_mood": (-4, -1),
    "neutral": (0, 0),
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

score_map = {
    "Energetic": 2, "Tired": -1, "Anxious": -2,
    "Happy": 2, "Okay": 0, "Low": -2,
    "Confident": 2, "Neutral": 0, "Insecure": -2,
    "Not at all": 2, "A little": -1, "Very much": -2
}

# -------------------- Endpoint --------------------
@app.post("/week2/emotion")
def detect_emotion(data: EmotionQuizRequest):
    # Calculate user score
    user_score = sum([score_map.get(ans, 0) for ans in data.answers.values()])

    detected_emotion = "neutral"
    for emotion, score_range in emotion_mapping.items():
        if score_range and len(score_range) == 2:
            if score_range[0] <= user_score <= score_range[1]:
                detected_emotion = emotion
                break

    prompt_category = category_mapping.get(detected_emotion, "neutral_support")

    # Filter dataset for matching prompts
    subset = df[
        (df["intent"] == prompt_category) &
        (df["cycle_phase"].str.lower() == data.cycle_phase.lower())
    ]

    if not subset.empty:
        prompt_row = subset.sample(1).iloc[0]
    else:
        fallback = df[df["intent"] == prompt_category]
        if not fallback.empty:
            prompt_row = fallback.sample(1).iloc[0]
        else:
            return {"error": "No matching prompt found."}

    return {
        "user_score": user_score,
        "detected_emotion": detected_emotion,
        "prompt_category": prompt_category,
        "cycle_phase": data.cycle_phase,
        "prompt_theme": prompt_row["theme"],
        "suggested_prompt": prompt_row["prompt"]
    }
