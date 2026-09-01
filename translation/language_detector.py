"""
Language Detection module for BharatTranslate-AI.
Combines Unicode script range analysis for accurate Indian language identification
with the `langdetect` library as a secondary detection engine.
"""

import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Fallback detection library
try:
    from langdetect import detect as langdetect_detect
    from langdetect import DetectorFactory
    DetectorFactory.seed = 0
    HAS_LANGDETECT = True
except ImportError:
    HAS_LANGDETECT = False
    logger.warning("langdetect library not installed. Language detection will rely on script heuristics.")


# Supported Indian & English Languages (ISO 639-1 / M2M100 codes)
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
}

# Unicode Script Ranges for Indian Languages
SCRIPT_RANGES: Dict[str, str] = {
    "ta": r'[\u0B80-\u0BFF]',  # Tamil
    "te": r'[\u0C00-\u0C7F]',  # Telugu
    "ml": r'[\u0D00-\u0D7F]',  # Malayalam
    "kn": r'[\u0C80-\u0CFF]',  # Kannada
    "bn": r'[\u0980-\u09FF]',  # Bengali
    "gu": r'[\u0A80-\u0AFF]',  # Gujarati
    "pa": r'[\u0A00-\u0A7F]',  # Punjabi (Gurmukhi)
    "hi": r'[\u0900-\u097F]',  # Devanagari (Hindi / Marathi)
}


class LanguageDetector:
    """
    Detects source language for input text using Unicode script regex
    and optional statistical language detection.
    """

    def __init__(self):
        self.supported_codes = set(SUPPORTED_LANGUAGES.keys())

    def detect_language(self, text: str) -> str:
        """
        Detects the 2-letter ISO language code of the input text.
        
        Args:
            text (str): Input string to analyze.

        Returns:
            str: 2-letter ISO language code (e.g. 'hi', 'ta', 'en'). Defaults to 'en'.
        """
        if not text or not text.strip():
            return "en"

        cleaned_text = text.strip()

        # Step 1: Script character frequency analysis for Indian scripts
        script_counts: Dict[str, int] = {}
        for lang_code, pattern in SCRIPT_RANGES.items():
            matches = len(re.findall(pattern, cleaned_text))
            if matches > 0:
                script_counts[lang_code] = matches

        if script_counts:
            # Pick the language code with the highest matching character count
            detected_by_script = max(script_counts, key=script_counts.get)
            
            # Devanagari script is shared between Hindi and Marathi.
            # Differentiate using langdetect if available.
            if detected_by_script == "hi" and HAS_LANGDETECT:
                try:
                    lang = langdetect_detect(cleaned_text)
                    if lang in ("hi", "mr"):
                        return lang
                except Exception:
                    pass
            return detected_by_script

        # Step 2: Fallback for Latin script (English) or general text via langdetect
        if HAS_LANGDETECT:
            try:
                lang = langdetect_detect(cleaned_text)
                if lang in self.supported_codes:
                    return lang
            except Exception as e:
                logger.debug(f"langdetect failure: {e}")

        # Default fallback if script is unrecognized or predominantly Latin
        return "en"

    def get_supported_languages(self) -> Dict[str, str]:
        """Returns dictionary of supported language codes and their full names."""
        return SUPPORTED_LANGUAGES
