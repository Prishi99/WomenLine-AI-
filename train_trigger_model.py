import json
import pickle
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Clean text function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

# Load your merged data file
with open("legal_qa_dataset_formatted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare data
X = [clean_text(d["text"]) for d in data]
y = [d["intent"] for d in data]

# Train model
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
classifier = RandomForestClassifier()
classifier.fit(X_vec, y)

# ✅ Save as a dictionary, not just the classifier!
with open("intent_model.pkl", "wb") as f:
    pickle.dump({"vectorizer": vectorizer, "classifier": classifier}, f)

print("✅ Model training and saving complete!")
