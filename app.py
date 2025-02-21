import streamlit as st
from utils import (
    text_to_speech, speech_to_text, grammar_and_spell_check,
    simplify_text, highlight_difficult_words, break_into_syllables,
    phonetic_pronunciation, pronounce_word, generate_personalized_content,
    generate_quiz, word_matching_game, provide_encouragement, track_progress
)

# Main Page
st.title("🧠 Dyslexia-Friendly Learning Assistant")

# Sidebar for Navigation
st.sidebar.header("🔧 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home", "📖 Real-Time Text Assistance", "📚 Improve Readability",
    "🔠 Pronunciation Support", "🎓 Personalized Learning", "🎮 Interactive Tools",
    "💬 Emotional Support", "📊 Progress Tracking"
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
    text = st.text_area("Enter text to read aloud:")
    if st.button("Convert to Speech"):
        audio_file = text_to_speech(text)
        st.audio(audio_file, format="audio/mp3")

    st.write("### Speech-to-Text")
    audio_file = st.file_uploader("Upload an audio file for speech-to-text:", type=["wav", "mp3"])
    if audio_file:
        text_output = speech_to_text(audio_file)
        st.write(f"Transcribed Text: {text_output}")

    st.write("### Grammar and Spell Check")
    text = st.text_area("Enter text to check grammar and spelling:")
    if st.button("Check Grammar and Spelling"):
        corrected_text = grammar_and_spell_check(text)
        st.write(f"Corrected Text: {corrected_text}")

# Improve Readability Page
elif page == "📚 Improve Readability":
    st.header("📚 Improve Readability")
    text = st.text_area("Enter text to simplify:")
    if st.button("Simplify Text"):
        simplified_text = simplify_text(text)
        highlighted_text = highlight_difficult_words(simplified_text)
        st.write(f"Simplified Text: {highlighted_text}")

# Pronunciation Support Page
elif page == "🔠 Pronunciation Support":
    st.header("🔠 Pronunciation Support")
    word = st.text_input("Enter a word to break into syllables:")
    if st.button("Break into Syllables"):
        syllables = break_into_syllables(word)
        st.write(f"Syllables: {syllables}")

    word = st.text_input("Enter a word for phonetic pronunciation:")
    if st.button("Get Phonetic Pronunciation"):
        pronunciation = phonetic_pronunciation(word)
        st.write(f"Phonetic Pronunciation: {pronunciation}")

    word = st.text_input("Enter a word to pronounce:")
    if st.button("Pronounce Word"):
        audio_file = pronounce_word(word)
        st.audio(audio_file, format="audio/mp3")

# Personalized Learning Page
elif page == "🎓 Personalized Learning":
    st.header("🎓 Personalized Learning")
    reading_level = st.selectbox("Select your reading level:", ["beginner", "intermediate", "advanced"])
    interests = st.text_input("Enter your interests (e.g., science, history, animals):")
    if st.button("Generate Personalized Content"):
        content = generate_personalized_content(reading_level, interests)
        st.write(f"Personalized Content: {content}")

# Interactive Tools Page
elif page == "🎮 Interactive Tools":
    st.header("🎮 Interactive Tools")
    text = st.text_area("Enter text to generate a quiz:")
    if st.button("Generate Quiz"):
        quiz = generate_quiz(text)
        st.write(f"Quiz: {quiz}")

    st.write("### Word Matching Game")
    if st.button("Start Word Matching Game"):
        words = word_matching_game()
        st.write(f"Match the words: {words}")

# Emotional Support Page
elif page == "💬 Emotional Support":
    st.header("💬 Emotional Support")
    if st.button("Get Encouragement"):
        encouragement = provide_encouragement()
        st.write(f"💖 {encouragement}")

# Progress Tracking Page
elif page == "📊 Progress Tracking":
    st.header("📊 Progress Tracking")
    user_id = st.text_input("Enter your user ID:")
    if st.button("Track Progress"):
        progress = track_progress(user_id)
        st.write(progress)
