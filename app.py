import streamlit as st
from utils import simplify_text, extract_text_from_image, text_to_speech, highlight_difficult_words

# Streamlit App
st.title("🧠 Dyslexia-Friendly AI Reading Assistant")

# Sidebar for customization
st.sidebar.header("🔧 User Preferences")
font_size = st.sidebar.slider("Font Size", 12, 30, 18)
background_color = st.sidebar.color_picker("Background Color", "#F5F5DC")  # Light beige for readability
text_color = st.sidebar.color_picker("Text Color", "#000000")

# TTS Controls
st.sidebar.header("🎤 Speech Settings")
speech_rate = st.sidebar.slider("Speech Rate", 50, 300, 130)
speech_volume = st.sidebar.slider("Speech Volume", 0.0, 1.0, 1.0)

# Apply Custom Styles
st.markdown(
    f"""
    <style>
    .stApp {{
        font-size: {font_size}px;
        background-color: {background_color};
        color: {text_color};
        font-family: 'OpenDyslexic', Arial, sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Input Section
st.header("✍️ Simplify & Learn Words")
input_text = st.text_area("Enter a sentence:", height=150)

if st.button("🔄 Simplify & Highlight"):
    simplified_text = simplify_text(input_text)
    highlighted_text = highlight_difficult_words(simplified_text)
    st.markdown(f"### ✅ Simplified Text\n{highlighted_text}")

    # Convert to speech
    audio_file = text_to_speech(simplified_text, rate=speech_rate, volume=speech_volume)
    st.audio(audio_file, format="audio/mp3")

# OCR Section
st.header("📷 Extract & Simplify from Image")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image_path = f"uploaded_image.{uploaded_file.name.split('.')[-1]}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extracted_text = extract_text_from_image(image_path)
    simplified_extracted_text = simplify_text(extracted_text)
    highlighted_extracted_text = highlight_difficult_words(simplified_extracted_text)

    st.markdown(f"### 📜 Extracted & Simplified Text\n{highlighted_extracted_text}")

    # Convert to speech
    audio_file = text_to_speech(simplified_extracted_text, rate=speech_rate, volume=speech_volume)
    st.audio(audio_file, format="audio/mp3")
