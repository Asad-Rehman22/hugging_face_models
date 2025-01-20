from flask import Blueprint, request, jsonify
from utils.translation import translate

bp = Blueprint('api', __name__)

@bp.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    
    # Input validation
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    text = data.get('text')
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'es')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    # Validate language codes
    supported_languages = ['en', 'es']
    if source_lang not in supported_languages or target_lang not in supported_languages:
        return jsonify({'error': f"Unsupported language pair. Supported languages: {supported_languages}"}), 400

    try:
        # Call the translation function
        translation = translate(text, source_lang, target_lang)
        
        if translation == "Unsupported language pair":
            return jsonify({'error': 'Unsupported language pair'}), 400

        return jsonify({
            'original_text': text,
            'source_language': source_lang,
            'target_language': target_lang,
            'translation': translation
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred during translation: {str(e)}'}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Translation API is running smoothly'})
