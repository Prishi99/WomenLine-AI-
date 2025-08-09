from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        if lang.startswith("hi"):
            return "hi"
        elif lang.startswith("mr"):
            return "mr"
        elif lang.startswith("ta"):
            return "ta"
        elif lang.startswith("bn"):
            return "bn"
        else:
            return "hi"  # fallback
    except:
        return "hi"
