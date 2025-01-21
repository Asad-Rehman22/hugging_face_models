from flask import Blueprint, request, jsonify
from translation_logic import translate  # Import the translation logic

# Define the blueprint
translation_routes = Blueprint("translation", __name__)

@translation_routes.route("/translate", methods=["POST"])
def translate_text():
    """
    Endpoint for translating text.
    Expects a JSON payload with 'text' and 'direction' fields.
    """
    data = request.get_json()
    text = data.get("text")
    direction = data.get("direction")  # e.g., 'en-to-es', 'es-to-en', etc.

    # Map translation direction to model names
    model_map = {
        "en-to-es": "Helsinki-NLP/opus-mt-en-es",
        "es-to-en": "Helsinki-NLP/opus-mt-es-en",
        "fr-to-en": "Helsinki-NLP/opus-mt-fr-en",
        "en-to-fr": "Helsinki-NLP/opus-mt-en-fr",
        "de-to-en": "Helsinki-NLP/opus-mt-de-en",
        "en-to-de": "Helsinki-NLP/opus-mt-en-de",
        "en-to-it": "Helsinki-NLP/opus-mt-en-it",
        "it-to-en": "Helsinki-NLP/opus-mt-it-en",
        "en-to-pt": "Helsinki-NLP/opus-mt-en-pt",
        "pt-to-en": "Helsinki-NLP/opus-mt-pt-en",
        "en-to-ru": "Helsinki-NLP/opus-mt-en-ru",
        "ru-to-en": "Helsinki-NLP/opus-mt-ru-en",
        "en-to-zh": "Helsinki-NLP/opus-mt-en-zh",
        "zh-to-en": "Helsinki-NLP/opus-mt-zh-en",
        "en-to-ja": "Helsinki-NLP/opus-mt-en-ja",
        "ja-to-en": "Helsinki-NLP/opus-mt-ja-en",
        "en-to-ar": "Helsinki-NLP/opus-mt-en-ar",
        "ar-to-en": "Helsinki-NLP/opus-mt-ar-en",
        "en-to-hi": "Helsinki-NLP/opus-mt-en-hi",
        "hi-to-en": "Helsinki-NLP/opus-mt-hi-en",
        "en-to-bn": "Helsinki-NLP/opus-mt-en-bn",
        "bn-to-en": "Helsinki-NLP/opus-mt-bn-en",
        "en-to-ta": "Helsinki-NLP/opus-mt-en-ta",
        "ta-to-en": "Helsinki-NLP/opus-mt-ta-en",
        "en-to-ko": "Helsinki-NLP/opus-mt-en-ko",
        "ko-to-en": "Helsinki-NLP/opus-mt-ko-en",
        "en-to-th": "Helsinki-NLP/opus-mt-en-th",
        "th-to-en": "Helsinki-NLP/opus-mt-th-en",
        "en-to-vi": "Helsinki-NLP/opus-mt-en-vi",
        "vi-to-en": "Helsinki-NLP/opus-mt-vi-en",
        "en-to-uk": "Helsinki-NLP/opus-mt-en-uk",
        "uk-to-en": "Helsinki-NLP/opus-mt-uk-en",
        "en-to-pl": "Helsinki-NLP/opus-mt-en-pl",
        "pl-to-en": "Helsinki-NLP/opus-mt-pl-en",
        "en-to-sv": "Helsinki-NLP/opus-mt-en-sv",
        "sv-to-en": "Helsinki-NLP/opus-mt-sv-en",
        "en-to-fi": "Helsinki-NLP/opus-mt-en-fi",
        "fi-to-en": "Helsinki-NLP/opus-mt-fi-en",
        "en-to-no": "Helsinki-NLP/opus-mt-en-no",
        "no-to-en": "Helsinki-NLP/opus-mt-no-en",
        "en-to-da": "Helsinki-NLP/opus-mt-en-da",
        "da-to-en": "Helsinki-NLP/opus-mt-da-en",
        "en-to-cs": "Helsinki-NLP/opus-mt-en-cs",
        "cs-to-en": "Helsinki-NLP/opus-mt-cs-en",
        "en-to-sl": "Helsinki-NLP/opus-mt-en-sl",
        "sl-to-en": "Helsinki-NLP/opus-mt-sl-en",
        "en-to-lt": "Helsinki-NLP/opus-mt-en-lt",
        "lt-to-en": "Helsinki-NLP/opus-mt-lt-en",
        "en-to-hu": "Helsinki-NLP/opus-mt-en-hu",
        "hu-to-en": "Helsinki-NLP/opus-mt-hu-en",
        "en-to-ro": "Helsinki-NLP/opus-mt-en-ro",
        "ro-to-en": "Helsinki-NLP/opus-mt-ro-en",
        "en-to-bg": "Helsinki-NLP/opus-mt-en-bg",
        "bg-to-en": "Helsinki-NLP/opus-mt-bg-en",
        "en-to-tr": "Helsinki-NLP/opus-mt-en-tr",
        "tr-to-en": "Helsinki-NLP/opus-mt-tr-en",
        "en-to-el": "Helsinki-NLP/opus-mt-en-el",
        "el-to-en": "Helsinki-NLP/opus-mt-el-en",
        "en-to-sq": "Helsinki-NLP/opus-mt-en-sq",
        "sq-to-en": "Helsinki-NLP/opus-mt-sq-en",
        "en-to-hr": "Helsinki-NLP/opus-mt-en-hr",
        "hr-to-en": "Helsinki-NLP/opus-mt-hr-en",
        "en-to-sr": "Helsinki-NLP/opus-mt-en-sr",
        "sr-to-en": "Helsinki-NLP/opus-mt-sr-en",
        "en-to-bg": "Helsinki-NLP/opus-mt-en-bg",
        "bg-to-en": "Helsinki-NLP/opus-mt-bg-en",
        "en-to-ur": "Helsinki-NLP/opus-mt-en-ur",
        "ur-to-en": "Helsinki-NLP/opus-mt-ur-en",
        "en-to-ur": "Helsinki-NLP/opus-mt-en-ur",
        "ur-to-en": "Helsinki-NLP/opus-mt-ur-en"
    }

    # Handling for Urdu-to-English and English-to-Urdu
    if not direction:
        if text.startswith(('ا', 'ب', 'پ')):  # Urdu starts with these characters
            direction = "ur-to-en"
        elif any(c.isalpha() for c in text):  # English check
            direction = "en-to-ur"
        else:
            return jsonify({"error": "Could not determine the translation direction."}), 400

    elif direction not in model_map:
        return jsonify({"error": "Invalid translation direction."}), 400

    model_name = model_map.get(direction)

    # Validate input
    if not text or not model_name:
        return jsonify({"error": "Invalid input. Provide both 'text' and a valid 'direction'."}), 400

    try:
        # Perform translation
        translated_text = translate(text, model_name)
        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500
