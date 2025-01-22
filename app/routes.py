from flask import Blueprint, request, jsonify
from translation_logic import translate
from transformers import pipeline
from textblob import TextBlob
import spacy
from flask_caching import Cache

# Load the Spacy language model for NER
nlp = spacy.load("D:\\Semester 4\\Lib\\site-packages\\spacy\\data\\en_core_web_sm")


# Flask-Caching configuration
cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Can be replaced with Redis or other options
}
cache = Cache(config=cache_config)

# Define the blueprint
translation_routes = Blueprint("translation", __name__)

# Centralized model map for translation
model_map = {
    "en-to-ar": "Helsinki-NLP/opus-mt-en-ar",
    "en-to-bg": "Helsinki-NLP/opus-mt-en-bg",
    "en-to-bn": "Helsinki-NLP/opus-mt-en-bn",
    "en-to-cs": "Helsinki-NLP/opus-mt-en-cs",
    "en-to-da": "Helsinki-NLP/opus-mt-en-da",
    "en-to-de": "Helsinki-NLP/opus-mt-en-de",
    "en-to-el": "Helsinki-NLP/opus-mt-en-el",
    "en-to-es": "Helsinki-NLP/opus-mt-en-es",
    "en-to-fi": "Helsinki-NLP/opus-mt-en-fi",
    "en-to-fr": "Helsinki-NLP/opus-mt-en-fr",
    "en-to-hi": "Helsinki-NLP/opus-mt-en-hi",
    "en-to-hr": "Helsinki-NLP/opus-mt-en-hr",
    "en-to-hu": "Helsinki-NLP/opus-mt-en-hu",
    "en-to-it": "Helsinki-NLP/opus-mt-en-it",
    "en-to-ja": "Helsinki-NLP/opus-mt-en-ja",
    "en-to-ko": "Helsinki-NLP/opus-mt-en-ko",
    "en-to-lt": "Helsinki-NLP/opus-mt-en-lt",
    "en-to-no": "Helsinki-NLP/opus-mt-en-no",
    "en-to-pl": "Helsinki-NLP/opus-mt-en-pl",
    "en-to-pt": "Helsinki-NLP/opus-mt-en-pt",
    "en-to-ro": "Helsinki-NLP/opus-mt-en-ro",
    "en-to-ru": "Helsinki-NLP/opus-mt-en-ru",
    "en-to-sq": "Helsinki-NLP/opus-mt-en-sq",
    "en-to-sr": "Helsinki-NLP/opus-mt-en-sr",
    "en-to-sl": "Helsinki-NLP/opus-mt-en-sl",
    "en-to-sv": "Helsinki-NLP/opus-mt-en-sv",
    "en-to-ta": "Helsinki-NLP/opus-mt-en-ta",
    "en-to-th": "Helsinki-NLP/opus-mt-en-th",
    "en-to-tr": "Helsinki-NLP/opus-mt-en-tr",
    "en-to-uk": "Helsinki-NLP/opus-mt-en-uk",
    "en-to-ur": "Helsinki-NLP/opus-mt-en-ur",
    "en-to-vi": "Helsinki-NLP/opus-mt-en-vi",
    "en-to-zh": "Helsinki-NLP/opus-mt-en-zh",
    "ar-to-en": "Helsinki-NLP/opus-mt-ar-en",
    "bg-to-en": "Helsinki-NLP/opus-mt-bg-en",
    "bn-to-en": "Helsinki-NLP/opus-mt-bn-en",
    "cs-to-en": "Helsinki-NLP/opus-mt-cs-en",
    "da-to-en": "Helsinki-NLP/opus-mt-da-en",
    "de-to-en": "Helsinki-NLP/opus-mt-de-en",
    "el-to-en": "Helsinki-NLP/opus-mt-el-en",
    "es-to-en": "Helsinki-NLP/opus-mt-es-en",
    "fi-to-en": "Helsinki-NLP/opus-mt-fi-en",
    "fr-to-en": "Helsinki-NLP/opus-mt-fr-en",
    "hi-to-en": "Helsinki-NLP/opus-mt-hi-en",
    "hr-to-en": "Helsinki-NLP/opus-mt-hr-en",
    "hu-to-en": "Helsinki-NLP/opus-mt-hu-en",
    "it-to-en": "Helsinki-NLP/opus-mt-it-en",
    "ja-to-en": "Helsinki-NLP/opus-mt-ja-en",
    "ko-to-en": "Helsinki-NLP/opus-mt-ko-en",
    "lt-to-en": "Helsinki-NLP/opus-mt-lt-en",
    "no-to-en": "Helsinki-NLP/opus-mt-no-en",
    "pl-to-en": "Helsinki-NLP/opus-mt-pl-en",
    "pt-to-en": "Helsinki-NLP/opus-mt-pt-en",
    "ro-to-en": "Helsinki-NLP/opus-mt-ro-en",
    "ru-to-en": "Helsinki-NLP/opus-mt-ru-en",
    "sq-to-en": "Helsinki-NLP/opus-mt-sq-en",
    "sr-to-en": "Helsinki-NLP/opus-mt-sr-en",
    "sl-to-en": "Helsinki-NLP/opus-mt-sl-en",
    "sv-to-en": "Helsinki-NLP/opus-mt-sv-en",
    "ta-to-en": "Helsinki-NLP/opus-mt-ta-en",
    "th-to-en": "Helsinki-NLP/opus-mt-th-en",
    "tr-to-en": "Helsinki-NLP/opus-mt-tr-en",
    "uk-to-en": "Helsinki-NLP/opus-mt-uk-en",
    "ur-to-en": "Helsinki-NLP/opus-mt-ur-en",
    "vi-to-en": "Helsinki-NLP/opus-mt-vi-en",
    "zh-to-en": "Helsinki-NLP/opus-mt-zh-en"
}

# Load a text correction model (optional)
text_correction = pipeline("text2text-generation", model="google/mt5-small")

# Load named entity recognition (NER) model
ner_model = pipeline("ner")

def autocorrect_sentence(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()  # This corrects the sentence
    return str(corrected_text)

@cache.memoize(timeout=3600)
def extract_entities(text):
    doc = nlp(text)  # Use Spacy's NER model
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def generate_meaningful_response(translated_text):
    response_generator = pipeline("text2text-generation", model="google/mt5-small")
    result = response_generator(translated_text, max_length=150, num_beams=5, early_stopping=True)
    return result[0]['generated_text']

@translation_routes.route("/translate", methods=["POST"])
def translate_text():
    """
    Endpoint for translating text.
    Expects a JSON payload with 'text' and 'direction' fields.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input. JSON data is required."}), 400

    text = data.get("text")
    direction = data.get("direction")

    if not text:
        return jsonify({"error": "Text for translation is required."}), 400

    if direction not in model_map:
        return jsonify({"error": "Invalid or missing translation direction."}), 400

    model_name = model_map.get(direction)

    try:
        # Check if the translation is cached
        cache_key = f"translated_text_{direction}_{text}"
        translated_text = cache.get(cache_key)

        if not translated_text:
            # Perform the translation
            translated_text = translate(text, model_name)
            cache.set(cache_key, translated_text, timeout=3600)  # Cache for 1 hour
            
        # Autocorrect the translated text
        corrected_translation = autocorrect_sentence(translated_text)
        
        # Extract named entities from the corrected translation
        entities = extract_entities(corrected_translation)
        
        # Generate a meaningful response
        meaningful_response = generate_meaningful_response(corrected_translation)
        
        return jsonify({
            "translated_text": corrected_translation,
            "entities": entities,
            "meaningful_response": meaningful_response
        }), 200
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500
