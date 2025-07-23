import streamlit as st
from language_handler import detect_language, get_prompt

st.set_page_config(page_title="Period CBT Prompt Recommender", page_icon="🩸")
st.title("🩸 Period CBT Prompt Recommender")
st.write("Welcome! Get a customized mental wellness prompt based on your feelings.")

# 🌐 User input
user_input = st.text_input("🗣️ How are you feeling today? (Type in your own language):")

if user_input:
    lang = detect_language(user_input)
    st.markdown(f"🌐 **Detected language**: `{lang.upper()}`")

    intent = st.selectbox("🎯 Choose intent", ["", "stress_relief", "mood_reframe", "body_acceptance"])
    theme = st.selectbox("🎨 Choose theme", ["", "anger", "sadness", "self_criticism", "fatigue"])
    cycle_phase = st.selectbox("🌀 Choose cycle phase", ["", "pre-period", "menstruation", "post-period"])

    if st.button("✨ Get Prompt"):
        prompt_text = get_prompt(
            preferred_lang=lang,
            intent=intent or None,
            theme=theme or None,
            cycle_phase=cycle_phase or None
        )
        st.markdown("🧘 **Here’s your recommended CBT prompt:**")
        st.markdown(f"👉 *{prompt_text}*")
