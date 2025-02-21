from PIL import Image
import pytesseract
import pyttsx3
import ollama
import os
import re

# Set Tesseract Path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to simplify text
def simplify_text(text):
    """
    Simplifies text using IBM Granite, underlines difficult words, and provides pronunciation.
    """
    response = ollama.generate(
        model="granite3.1-dense:2b",
        prompt=f"""
        Rewrite this text in **simple words** for someone with dyslexia. 
        - Use **short sentences** and **easy words**.
        - **Find difficult words** and highlight them with asterisks (**word**).
        - Break tough words into syllables (example: "phenomenon" → "phe-no-me-non").
        - Give **meaning** for tough words.
        - Ensure it's **engaging and fun to read**.
        
        Text: {text}
        """
    )
    return response['response']

# Function to extract text from an image
def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR (Tesseract).
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

# Function to convert text to speech with better pronunciation
def text_to_speech(text, output_file="output.mp3", rate=130, volume=1.0):
    """
    Convert text to speech using pyttsx3 with adjustable speed & volume.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file

# Function to extract & underline tough words
def highlight_difficult_words(text):
    """
    Identify hard words and underline them.
    """
    hard_words = [word for word in text.split() if len(word) > 7]  # Example logic: words > 7 letters
    for word in hard_words:
        text = text.replace(word, f"**{word}**")  # Bold for readability
    return text
