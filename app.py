import os
import streamlit as st
from utils import (
    text_to_speech, speech_to_text, grammar_and_spell_check,
    simplify_text, highlight_difficult_words, break_into_syllables,
    phonetic_pronunciation, generate_personalized_content, generate_quiz,
    provide_encouragement, 
    detect_complex_words, explain_word,
    get_phonetic, generate_word_audio
)

# Main Page
st.title("🧠 Dyslexia-Friendly Learning Assistant")

# Sidebar for Navigation
st.sidebar.header("🔧 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home", "📖 Real-Time Text Assistance", "📚 Improve Readability",
    "🔠 Pronunciation Support", "🎓 Personalized Learning", "🎮 Interactive Tools",
    "💬 Emotional Support"
])

# Apply Custom Styles
st.markdown(
    """
    <style>
    .stApp {
        font-family: 'OpenDyslexic', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Home Page
if page == "🏠 Home":
    st.write("""
    ### Welcome to the Dyslexia-Friendly Learning Assistant!
    This app is designed to help individuals with dyslexia by providing:
    - **Real-time text assistance** with text-to-speech and speech-to-text.
    - **Improved readability** with simplified text and dyslexia-friendly fonts.
    - **Pronunciation support** with phonetic breakdowns and audio hints.
    - **Personalized learning** tailored to your needs.
    - **Interactive tools** like quizzes and games.
    - **Emotional support** with encouragement and progress tracking.
    """)

# Real-Time Text Assistance Page
elif page == "📖 Real-Time Text Assistance":
    st.header("📖 Real-Time Text Assistance")
    
    # Text-to-Speech
    text = st.text_area("Enter text to read aloud:")
    if st.button("Convert to Speech"):
        if not text.strip():
            st.warning("Please enter some text to convert to speech.")
        else:
            audio_file = text_to_speech(text)
            if audio_file.startswith("Error"):
                st.error(audio_file)
            else:
                st.audio(audio_file, format="audio/mp3")

    # Speech-to-Text
    st.write("### Speech-to-Text")
    audio_file = st.file_uploader("Upload an audio file for speech-to-text:", type=["wav", "mp3"])
    if audio_file:
        if audio_file.size > 10 * 1024 * 1024:  # 10MB limit
            st.error("File size too large! Please upload files smaller than 10MB.")
        else:
            text_output = speech_to_text(audio_file)
            if text_output.startswith("Error"):
                st.error(text_output)
            else:
                st.write(f"Transcribed Text: {text_output}")

    # Grammar Check
    st.write("### Grammar and Spell Check")
    text = st.text_area("Enter text to check grammar and spelling:")
    if st.button("Check Grammar and Spelling"):
        if not text.strip():
            st.warning("Please enter some text to check.")
        else:
            corrected_text = grammar_and_spell_check(text)
            if corrected_text.startswith("Error"):
                st.error(corrected_text)
            else:
                st.write(f"Corrected Text: {corrected_text}")

# Improve Readability Page
elif page == "📚 Improve Readability":
    st.header("📚 Improve Readability")
    text = st.text_area("Enter text to simplify:")
    if st.button("Simplify Text"):
        if not text.strip():
            st.warning("Please enter some text to simplify.")
        else:
            simplified_text = simplify_text(text)
            if simplified_text.startswith("Error"):
                st.error(simplified_text)
            else:
                highlighted_text = highlight_difficult_words(simplified_text)
                st.write(f"Simplified Text: {highlighted_text}")

# Pronunciation Support Page
elif page == "🔠 Pronunciation Support":
    st.header("🔠 Pronunciation Support")
    
    # Main Analysis
    st.subheader("AI-Powered Pronunciation Guide")
    text_input = st.text_area("Enter text to analyze:", height=150)
    
    if st.button("Analyze Text"):
        if not text_input.strip():
            st.warning("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing text..."):
                input_words = set(text_input.lower().split())
                complex_words = detect_complex_words(text_input)
                
                if isinstance(complex_words, list):
                    # Filter valid words
                    valid_words = [w for w in complex_words if w.lower() in input_words]
                    
                    if len(valid_words) > 0:
                        st.success(f"Found {len(valid_words)} complex words:")
                        for word in valid_words:
                            with st.expander(f"🔍 {word}", expanded=True):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    explanation = explain_word(word)
                                    if explanation.startswith("Error"):
                                        st.error(explanation)
                                    else:
                                        st.markdown(f"**Simple Explanation:**\n{explanation}")
                                    
                                    phonetic = get_phonetic(word)
                                    if phonetic.startswith("/pho-netic-error"):
                                        st.error(phonetic)
                                    else:
                                        st.markdown(f"**Phonetic Spelling:**\n/{phonetic}/")
                                
                                with col2:
                                    audio_file = generate_word_audio(word)
                                    if audio_file.startswith("Error"):
                                        st.error(audio_file)
                                    else:
                                        st.audio(audio_file, format="audio/mp3")
                                        if os.path.exists(audio_file):
                                            os.remove(audio_file)
                    else:
                        st.warning("No complex words found! Text is dyslexia-friendly 🎉")
                else:
                    st.error(f"Analysis failed: {complex_words}")

    # Individual Word Tools
    st.divider()
    st.subheader("Individual Word Tools")
    word = st.text_input("Enter a single word for analysis:")
    if word:
        if not word.isalpha():
            st.error("Please enter a single word without numbers or special characters.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Syllables**")
                syllables = break_into_syllables(word)
                st.code(syllables if not syllables.startswith("Error") else "⚠️ Error analyzing syllables")
            
            with col2:
                st.write("**Phonetic**")
                phonetic = get_phonetic(word)
                st.code(phonetic if not phonetic.startswith("/pho-netic-error") else "⚠️ Phonetic error")
            
            with col3:
                st.write("**Pronunciation**")
                audio_file = generate_word_audio(word)
                if audio_file.startswith("Error"):
                    st.error(audio_file)
                else:
                    st.audio(audio_file, format="audio/mp3")
                    if os.path.exists(audio_file):
                        os.remove(audio_file)

# Personalized Learning Page
elif page == "🎓 Personalized Learning":
    st.header("🎓 Personalized Learning")
    reading_level = st.selectbox("Select your reading level:", ["beginner", "intermediate", "advanced"])
    interests = st.text_input("Enter your interests (e.g., science, history, animals):")
    if st.button("Generate Personalized Content"):
        if not interests.strip():
            st.warning("Please enter your interests to generate content.")
        else:
            content = generate_personalized_content(reading_level, interests)
            if content.startswith("Error"):
                st.error(content)
            else:
                st.write(f"Personalized Content: {content}")

# Interactive Tools Page
elif page == "🎮 Interactive Tools":
    st.header("🎮 Interactive Tools")
    text = st.text_area("Enter text to generate a quiz:")
    if st.button("Generate Quiz"):
        if not text.strip():
            st.warning("Please enter some text to create a quiz.")
        else:
            quiz = generate_quiz(text)
            if quiz.startswith("Error"):
                st.error(quiz)
            else:
                st.write(f"Quiz: {quiz}")

# Emotional Support Page
elif page == "💬 Emotional Support":
    st.header("💬 Emotional Support")
    if st.button("Get Encouragement"):
        encouragement = provide_encouragement()
        if encouragement.startswith("Error"):
            st.error("Could not generate encouragement. Please try again.")
        else:
            st.write(f"💖 {encouragement}")