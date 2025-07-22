from language_detector import detect_language, get_prompt

def run_prompt_demo():
    print("🩸 Welcome to Period CBT Prompt Recommender")
    
    # Step 1: Simulate user input
    user_input = input("🗣️  How are you feeling today? (type in your own language):\n> ")

    # Step 2: Detect language
    lang_code = detect_language(user_input)
    print(f"🌐 Detected language: {lang_code.upper()}")

    # Step 3: Optional intent filter
    intent = input("🎯 Choose intent (stress_relief / mood_reframe / body_acceptance) or press Enter to skip:\n> ").strip()
    if intent == "":
        intent = None

    # Step 4: Optional cycle phase
    phase = input("🌀 Choose cycle phase (pre-period / menstruation / post-period) or press Enter to skip:\n> ").strip()
    if phase == "":
        phase = None

    # Step 5: Get prompt
    prompt = get_prompt(preferred_lang=lang_code, intent=intent, cycle_phase=phase)

    # Step 6: Show result
    print("\n🧘 Here’s your recommended CBT prompt:")
    print(f"👉 {prompt}")

if __name__ == "__main__":
    run_prompt_demo()
