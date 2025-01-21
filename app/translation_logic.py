from transformers import pipeline

# Load pre-trained models directly
def load_model(model_name):
    return pipeline("translation", model=model_name)

def translate(text, model_name):
    model = load_model(model_name)
    result = model(text)
    return result[0]["translation_text"]
