from PIL import Image
import pytesseract
import pyttsx3
import ollama
import os

# Set Tesseract Path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def simplify_text(text):
    """
    Simplify text using IBM Granite 3.1-dense:2b with a more user-friendly prompt.
    """
    response = ollama.generate(
        model="granite3.1-dense:2b",
        prompt=f"""
        Rewrite this text using very simple and clear words so that a person with dyslexia can easily understand it.

        - Use **short sentences** and **common words**.
        - Avoid difficult vocabulary and complex ideas.
        - Explain in a **friendly and supportive **, like a teacher helping a student.
        - If needed, **break down complicated ideas into step-by-step explanations**.

        Here is the text: {text}
        """
    )
    simplified_text = response['response']
    return simplified_text

def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR (Tesseract).
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

def text_to_speech(text, output_file="output.mp3", rate=150, volume=1.0):
    """
    Convert text to speech using pyttsx3 with a female voice for better clarity.
    """
    engine = pyttsx3.init()
    
    # Set female voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    engine.setProperty('rate', rate)  # Speed of speech
    engine.setProperty('volume', volume)  # Volume level (0.0 to 1.0)
    
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file
