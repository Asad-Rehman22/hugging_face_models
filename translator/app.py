import gradio as gr
from transformers import pipeline

# Load translation pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-es")

def translate_text(text):
    result = translator(text, max_length=400)
    return result[0]["translation_text"]

# Gradio interface
iface = gr.Interface(
    fn=translate_text,
    inputs="text",
    outputs="text",
    title="English to Spanish Translator",
    description="Translate English sentences into Spanish using a pre-trained NLP model."
)

iface.launch()
