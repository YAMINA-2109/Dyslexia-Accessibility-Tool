import streamlit as st
from utils import simplify_text, extract_text_from_image, text_to_speech

# Streamlit App
st.title("🧠 AI-Powered Dyslexia Accessibility Tool")

# Sidebar for customization
st.sidebar.header("🔧 User Preferences")
font_size = st.sidebar.slider("Font Size", 12, 24, 16)
font_type = st.sidebar.selectbox("Font Type", ["Arial", "OpenDyslexic", "Comic Sans"])
background_color = st.sidebar.color_picker("Background Color", "#FFFFFF")
text_color = st.sidebar.color_picker("Text Color", "#000000")

# TTS Controls
st.sidebar.header("🎤 Text-to-Speech Settings")
speech_rate = st.sidebar.slider("Speech Rate", 50, 300, 150)
speech_volume = st.sidebar.slider("Speech Volume", 0.0, 1.0, 1.0)

# Apply custom styles
st.markdown(
    f"""
    <style>
    .stApp {{
        font-size: {font_size}px;
        font-family: {font_type}, sans-serif;
        background-color: {background_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Input Section
st.header("✍️ Simplify Text")
input_text = st.text_area("Enter your text here:", height=200)

if st.button("🔄 Simplify Text"):
    simplified_text = simplify_text(input_text)
    st.write("### ✅ Simplified Text")
    st.write(simplified_text)

    # Convert to speech
    audio_file = text_to_speech(simplified_text, rate=speech_rate, volume=speech_volume)
    st.audio(audio_file, format="audio/mp3")

# OCR Section
st.header("📷 Extract Text from Image")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image_path = f"uploaded_image.{uploaded_file.name.split('.')[-1]}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extracted_text = extract_text_from_image(image_path)
    st.write("### 📜 Extracted Text")
    st.write(extracted_text)

    # Simplify Extracted Text
    simplified_extracted_text = simplify_text(extracted_text)
    st.write("### ✅ Simplified Extracted Text")
    st.write(simplified_extracted_text)

    # Convert to speech
    audio_file = text_to_speech(simplified_extracted_text, rate=speech_rate, volume=speech_volume)
    st.audio(audio_file, format="audio/mp3")
