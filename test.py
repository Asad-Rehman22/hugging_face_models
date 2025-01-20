from transformers import pipeline

def translate_text(text, source_lang, target_lang):
    # Load the translation pipeline from Hugging Face
    translation_pipeline = pipeline("translation", model=f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}')
    
    # Perform the translation
    translated_text = translation_pipeline(text)[0]['translation_text']
    return translated_text

def main():
    # Paragraph to be translated
    paragraph_to_translate = (
        "Once upon a time, in a small village surrounded by lush green hills, lived a kind and humble farmer named Tom. "
        "Every day, he would wake up before sunrise, tend to his crops with care, and share his harvest with the villagers. "
        "One evening, as Tom was walking home, he stumbled upon an old, worn-out book lying by the side of the path. "
        "Curious, he picked it up and found that it was filled with stories of magical lands and enchanted creatures. "
        "Little did he know, this book would lead him on the most incredible adventure of his life."
    )
    
    # Translate from English to Spanish
    translated_to_es = translate_text(paragraph_to_translate, source_lang='en', target_lang='es')
    print(f"EN -> ES: {translated_to_es}")
    
    # Write the output to 'output_es.txt'
    with open('output_es.txt', 'w') as file:
        file.write(translated_to_es)

if __name__ == "__main__":
    main()
