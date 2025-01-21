from transformers import pipeline

# Cache for storing loaded models
model_cache = {}

def load_model(model_name):
    """
    Load and cache the model to avoid reloading it multiple times.
    """
    if model_name not in model_cache:
        model_cache[model_name] = pipeline("translation", model=model_name)
    return model_cache[model_name]

def translate(text, model_name):
    """
    Perform translation using the specified model.
    """
    model = load_model(model_name)
    result = model(text, max_length=400)
    return result[0]["translation_text"]
