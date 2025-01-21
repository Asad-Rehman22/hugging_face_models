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
    direction = data.get("direction")  # e.g., 'en-to-es' or 'es-to-en'

    # Map translation direction to model names
    model_map = {
        "en-to-es": "Helsinki-NLP/opus-mt-en-es",
        "es-to-en": "Helsinki-NLP/opus-mt-es-en"
    }
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
