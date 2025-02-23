from PIL import Image
import pytesseract
import pyttsx3
import ollama
import random
import time
from g2p_en import G2p
import tempfile
import os
import comtypes.client  # For COM initialization
from gtts import gTTS  # Alternative TTS library
import nltk
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Ensure NLTK data is downloaded
try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng')

# Set Tesseract Path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Predefined datasets for auto-generated text
SIMPLE_SENTENCES = [
    "The cat sat on the mat.",
    "Birds fly in the sky.",
    "I like to eat apples.",
    "The sun is bright and warm.",
    "Dogs are loyal and friendly.",
]

COMPLEX_SENTENCES = [
    "The phenomenon of quantum entanglement is fascinating.",
    "Photosynthesis is the process by which plants make food.",
    "The Eiffel Tower is a famous landmark in Paris.",
    "Global warming is affecting our planet.",
    "Artificial intelligence is transforming industries.",
]

# Real-Time Text Assistance
def text_to_speech(text, output_file="output.mp3", rate=130, volume=1.0):
    """
    Convert text to speech using pyttsx3 with adjustable speed & volume.
    """
    # Initialize COM
    comtypes.CoInitialize()
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        return output_file
    except Exception as e:
        return f"Error in text-to-speech: {e}"
    finally:
        # Uninitialize COM
        comtypes.CoUninitialize()

def speech_to_text(audio_file):
    """
    Convert speech to text using a speech recognition API.
    """
    # Placeholder for speech-to-text functionality
    return "This is a placeholder for speech-to-text output."

def grammar_and_spell_check(text):
    """
    Check grammar and spelling using AI.
    """
    try:
        response = ollama.generate(
            model="granite3.1-dense:2b",  # Use the correct model
            prompt=f"""
            Correct the grammar and spelling of this text:
            {text}
            """
        )
        return response['response']
    except Exception as e:
        return f"Error in grammar and spell check: {e}"

# Improve Readability
def simplify_text(text):
    """
    Simplify text for better readability.
    """
    try:
        response = ollama.generate(
            model="granite3.1-dense:2b",  # Use the correct model
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
    except Exception as e:
        return f"Error in text simplification: {e}"

def highlight_difficult_words(text):
    """
    Highlight difficult words in the text.
    """
    hard_words = [word for word in text.split() if len(word) > 7]  # Example logic: words > 7 letters
    for word in hard_words:
        text = text.replace(word, f"**{word}**")  # Bold for readability
    return text

# Pronunciation and Phonetic Support
def break_into_syllables(word):
    """
    Break a word into syllables for easier pronunciation.
    """
    vowels = "aeiouy"
    syllable_count = 0
    syllables = []
    current_syllable = ""
    for i, char in enumerate(word):
        current_syllable += char
        if char in vowels:
            syllable_count += 1
            if i != len(word) - 1 and word[i + 1] not in vowels:
                syllables.append(current_syllable)
                current_syllable = ""
    if current_syllable:
        syllables.append(current_syllable)
    return "-".join(syllables)

def phonetic_pronunciation(word):
    """
    Provide phonetic pronunciation for a word.
    """
    try:
        response = ollama.generate(
            model="granite3.1-dense:2b",  # Use the correct model
            prompt=f"""
            Provide the phonetic pronunciation for this word:
            {word}
            """
        )
        return response['response']
    except Exception as e:
        return f"Error in phonetic pronunciation: {e}"

# Personalization and Adaptive Learning
def generate_personalized_content(reading_level, interests):
    """
    Generate personalized content based on reading level and interests.
    """
    if reading_level == "beginner":
        return random.choice(SIMPLE_SENTENCES)
    elif reading_level == "intermediate":
        return random.choice(COMPLEX_SENTENCES)
    else:
        return "Personalized content not available for this level."

# Gamification and Interactive Learning
def generate_quiz(text):
    """
    Generate a quiz based on the provided text.
    """
    try:
        response = ollama.generate(
            model="granite3.1-dense:2b",  # Use the correct model
            prompt=f"""
            Generate a quiz with 3 questions based on this text:
            {text}
            """
        )
        return response['response']
    except Exception as e:
        return f"Error in quiz generation: {e}"

# Emotional and Cognitive Support
def provide_encouragement():
    """
    Provide gentle encouragement to the user.
    """
    encouragements = [
        "Great job! Keep going!",
        "You're doing amazing!",
        "Every mistake is a step toward learning!",
        "You've got this!",
    ]
    return random.choice(encouragements)

# Pronunciation and Meaning Functions
def detect_complex_words(text):
    """Identify complex words using dyslexia-focused criteria"""
    try:
        # Preserve original words and order
        original_words = text.split()
        base_words_lower = {word.lower() for word in original_words}
        
        # Dyslexia-focused prompt
        prompt = f"""ANALYZE THIS TEXT THROUGH A DYSLEXIC READER'S PERSPECTIVE:
        {text}
        
        IDENTIFY WORDS THAT:
        1. List EXACT words as they appear
        2. Have uncommon letter patterns (e.g., 'ough' in 'through')
        3. Contain silent letters
        4. Technical/scientific terms
        5. Comma-separated
        6. Have 3+ syllables
        7. Are homophones (words that sound alike)
        8. Maintain original order
        9. Have irregular spellings
        
        RETURN COMMA-SEPARATED WORDS IN ORIGINAL ORDER"""
        
        response = ollama.generate(
            model="granite3.1-dense:2b",
            prompt=prompt
        )
        
        # Combine model detection with syllable count
        detected_words = []
        seen = set()
        
        # First pass: Model's suggestions
        for word in response['response'].split(', '):
            clean_word = word.strip()
            lower_word = clean_word.lower()
            if (clean_word and
                lower_word in base_words_lower and
                lower_word not in seen):
                detected_words.append(clean_word)
                seen.add(lower_word)
        
        # Second pass: Programmatic checks
        for word in original_words:
            lower_word = word.lower()
            if (lower_word not in seen and
                (count_syllables(word) >= 3 or  # Custom syllable counter
                 has_silent_letters(word) or    # Add helper functions
                 is_irregular_spelling(word))):
                detected_words.append(word)
                seen.add(lower_word)
        
        return detected_words

    except Exception as e:
        logging.error(f"Detection error: {str(e)}")
        return []
    
def count_syllables(word):
    """Simple syllable counter for English words"""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1
    return max(1, count)  # All words have at least 1 syllable

def has_silent_letters(word):
    """Check common silent letter patterns"""
    silent_patterns = {
        'kn', 'gn', 'wr', 'mb', 'mn',
        'gh', 'rh', 'wh', 'lk', 'alf'
    }
    return any(pattern in word.lower() for pattern in silent_patterns)

def is_irregular_spelling(word):
    """Check for common irregular spelling patterns"""
    irregulars = {
        'ough', 'ei', 'ie', 'tion', 'sion',
        'cian', 'tch', 'dge', 'gue', 'que'
    }
    return any(pattern in word.lower() for pattern in irregulars)

def explain_word(word):
    """Get simple explanation using Granite"""
    try:
        response = ollama.generate(
            model="granite3.1-dense:2b",
            prompt=f"Explain '{word}' simply for a dyslexic reader. Use 1 short sentence."
        )
        return response['response']
    except Exception as e:
        return f"Error explaining word: {e}"

def get_phonetic(word):
    """Get phonetic pronunciation using g2p-en"""
    try:
        g2p = G2p()
        phonemes = g2p(word)
        return ' '.join(phonemes)
    except Exception as e:
        return f"Error generating phonetic: {e}"

def generate_word_audio(word):
    """Create pronunciation audio with timestamp"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
            tts = gTTS(text=word, lang='en', slow=True)
            tts.save(tf.name)
            return tf.name
    except Exception as e:
        return f"Error generating audio: {e}"