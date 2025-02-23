import streamlit as st
import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel 

# 🏗️ Load the fine-tuned model and tokenizer
@st.cache_resource
def load_model():
    base_model = AutoModelForCausalLM.from_pretrained(
        "ibm-granite/granite-3.0-8b-instruct",
        torch_dtype=torch.bfloat16,  # Optimizing memory usage
        device_map="auto"
    )

    # Load fine-tuned weights
    model = PeftModel.from_pretrained(base_model, "IAyamina/IBM_hackathonIA_granite_finetuned_dyslexia")

    tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.0-8b-instruct")

    return model, tokenizer

# Load the model and tokenizer
model, tokenizer = load_model()

# ✨ Function to simplify text
def simplify_text(text):
    prompt = f"Rewrite the following sentence in a simpler way: {text}"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")  # Move to GPU if available
    outputs = model.generate(**inputs, max_new_tokens=100)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # ✅ Extract only the part after "Answer:"
    match = re.search(r"Answer:\s*(.*)", generated_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # ✅ Return only the simplified sentence
    else:
        return generated_text.strip()  # ✅ Return the cleaned output

# 🎨 Streamlit Interface
st.title("🧠 AI-Powered Dyslexia Text Simplifier")
st.write("Enter a complex text, and the model will simplify it for better readability!")

# User input text box
user_input = st.text_area("Enter your complex text:", "The proliferation of computational methodologies...")

if st.button("Simplify Text"):
    with st.spinner("Processing... 🔄"):
        simplified_text = simplify_text(user_input)
    st.success("✅ Simplification Complete!")
    st.write("**Simplified Text:**")
    st.write(simplified_text)
