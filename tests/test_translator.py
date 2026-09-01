"""
Unit tests for BharatTranslate-AI translation module and language detector.
"""

import unittest
from translation.language_detector import LanguageDetector, SUPPORTED_LANGUAGES
from translation.translator import Translator


class TestLanguageDetector(unittest.TestCase):
    """Test suite for LanguageDetector module."""

    def setUp(self):
        self.detector = LanguageDetector()

    def test_supported_languages(self):
        """Test that all 10 target languages are present."""
        expected_codes = {"en", "hi", "ta", "te", "ml", "kn", "bn", "mr", "gu", "pa"}
        self.assertEqual(set(SUPPORTED_LANGUAGES.keys()), expected_codes)

    def test_script_detection_hindi(self):
        """Test Devanagari script detection (Hindi)."""
        text = "नमस्ते दुनिया"
        detected = self.detector.detect_language(text)
        self.assertIn(detected, ["hi", "mr"])

    def test_script_detection_tamil(self):
        """Test Tamil script detection."""
        text = "வணக்கம் உலகம்"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "ta")

    def test_script_detection_telugu(self):
        """Test Telugu script detection."""
        text = "నమస్కారం ప్రపంచం"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "te")

    def test_script_detection_malayalam(self):
        """Test Malayalam script detection."""
        text = "നമസ്കാരം ലോകമേ"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "ml")

    def test_script_detection_kannada(self):
        """Test Kannada script detection."""
        text = "ನಮಸ್ಕಾರ ಪ್ರಪಂಚ"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "kn")

    def test_script_detection_bengali(self):
        """Test Bengali script detection."""
        text = "হ্যালো বিশ্ব"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "bn")

    def test_script_detection_gujarati(self):
        """Test Gujarati script detection."""
        text = "નમસ્તે દુનિયા"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "gu")

    def test_script_detection_punjabi(self):
        """Test Punjabi (Gurmukhi) script detection."""
        text = "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "pa")

    def test_script_detection_english(self):
        """Test English text detection."""
        text = "Hello world! Welcome to BharatTranslate AI."
        detected = self.detector.detect_language(text)
        self.assertEqual(detected, "en")


class TestTranslatorStructure(unittest.TestCase):
    """Test suite for Translator structure."""

    def test_translator_init(self):
        """Test translator initialization without loading model weights."""
        translator = Translator()
        self.assertIsNotNone(translator.device)
        self.assertEqual(translator.model_name, "facebook/m2m100_418M")


if __name__ == "__main__":
    unittest.main()
