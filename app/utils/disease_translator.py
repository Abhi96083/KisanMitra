"""
Disease Translator Module
Handles multilingual disease descriptions without modifying ML inference logic
"""

import json
import os
from flask import session

# Path to disease translations
DISEASE_TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), 'disease_translations')

def load_disease_translations(lang_code='en'):
    """
    Load disease translations for the specified language.
    Falls back to English if language file not found.
    """
    lang_file = os.path.join(DISEASE_TRANSLATIONS_DIR, f'diseases_{lang_code}.json')
    
    # Try to load requested language
    if os.path.exists(lang_file):
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Fallback to English
    english_file = os.path.join(DISEASE_TRANSLATIONS_DIR, 'diseases_en.json')
    try:
        with open(english_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def get_disease_description(disease_name, lang_code=None):
    """
    Get disease description in the specified language.
    If no language specified, uses the session language preference.
    
    Args:
        disease_name: The disease key (e.g., 'Apple___Apple_scab')
        lang_code: Language code ('en', 'hi', 'kn'). If None, uses session language.
    
    Returns:
        Disease description in the requested language (HTML format)
    """
    if lang_code is None:
        lang_code = session.get('language', 'en')
    
    if lang_code not in ['en', 'hi', 'kn']:
        lang_code = 'en'
    
    translations = load_disease_translations(lang_code)
    
    # Return translated description or empty string if not found
    return translations.get(disease_name, '')

def translate_disease_output(disease_name, lang_code=None):
    """
    Wrapper function to get disease description.
    Designed to work seamlessly with the existing predict_image flow.
    
    Args:
        disease_name: The disease key from ML model prediction
        lang_code: Language code (optional)
    
    Returns:
        HTML formatted disease description in the requested language
    """
    return get_disease_description(disease_name, lang_code)
