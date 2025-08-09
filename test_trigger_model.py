import pickle
import json
import re
import string

# 🧹 Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

# 📂 Load prompt map
def load_prompt_map(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading prompt map: {e}")
        return {}

# 🔌 Load model
with open("intent_model.pkl", "rb") as f:
    model_data = pickle.load(f)

vectorizer = model_data["vectorizer"]
classifier = model_data["classifier"]

# 🧠 Prediction
def process_query_ml_trigger(user_query, prompt_map):
    clean_query = clean_text(user_query)
    query_vec = vectorizer.transform([clean_query])
    predicted_intent = classifier.predict(query_vec)[0]
    response = prompt_map.get(predicted_intent, "❓ कोई उपयुक्त उत्तर नहीं मिला।")
    return response, predicted_intent

# ▶️ Test
if __name__ == "__main__":
    prompt_map = load_prompt_map("intent_prompt_map.json")
    query = "मुझे तलाक चाहिए"
    response, intent = process_query_ml_trigger(query, prompt_map)
    print("Query:", query)
    print("Intent:", intent)
    print("Response:", response)
