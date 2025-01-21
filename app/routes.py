from flask import Blueprint, request, jsonify
from translation_logic import translate  # Updated import

translation_routes = Blueprint("translation", __name__)

@translation_routes.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    text = data.get("text")
    direction = data.get("direction")  # e.g., 'en-to-es' or 'es-to-en'

    # Map translation direction to model name
    model_map = {
        "en-to-es": "Helsinki-NLP/opus-mt-en-es",
        "es-to-en": "Helsinki-NLP/opus-mt-es-en"
    }
    model_name = model_map.get(direction)

    if not text or not model_name:
        return jsonify({"error": "Invalid input"}), 400

    try:
        translated_text = translate(text, model_name)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
