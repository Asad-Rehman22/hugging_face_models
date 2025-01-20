from transformers import pipeline
from utils.cache import set_to_cache, get_from_cache

# Load the translation models from Hugging Face
translator_en_to_es = pipeline('translation_en_to_es', model='Helsinki-NLP/opus-mt-en-es')
translator_es_to_en = pipeline('translation_es_to-en', model='Helsinki-NLP/opus-mt-es-en')

def translate(text, source_lang='en', target_lang='es'):
    cache_key = f"{source_lang}_{target_lang}_{text}"
    
    # Check if translation result is in cache
    cached_translation = get_from_cache(cache_key)
    if cached_translation:
        return cached_translation
    
    if source_lang == 'en' and target_lang == 'es':
        translation = translator_en_to_es(text)
    elif source_lang == 'es' and target_lang == 'en':
        translation = translator_es_to_en(text)
    else:
        return "Unsupported language pair"
    
    if translation:
        # Cache the translated result
        set_to_cache(cache_key, translation, timeout=3600)  # Cache for 1 hour
    
    return translation

# Optional: More complex handling can be done to return detailed error messages
