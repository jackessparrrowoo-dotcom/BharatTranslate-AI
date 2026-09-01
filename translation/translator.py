"""
Translation engine wrapper powered by PyTorch & Hugging Face M2M100 model.
Supports English and major Indian languages.
"""

import os
import logging
from typing import Dict, Any, Optional

from .language_detector import LanguageDetector, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

# Pretrained Hugging Face Multilingual Translation Model
DEFAULT_MODEL_NAME = "facebook/m2m100_418M"


class Translator:
    """
    Deep Learning Translation Service using Hugging Face M2M100 and PyTorch.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, cache_dir: Optional[str] = None):
        """
        Initializes the PyTorch Hugging Face translator wrapper.

        Args:
            model_name (str): Hugging Face model repository name.
            cache_dir (str, optional): Custom path for caching model weights.
        """
        self.model_name = model_name
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        
        self.device = None
        self._init_device()

        self.tokenizer = None
        self.model = None
        self.detector = LanguageDetector()

    def _init_device(self):
        """Initializer for PyTorch device."""
        if self.device is None:
            try:
                import torch
                self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                logger.info(f"Translator hardware backend initialized on device: {self.device}")
            except ImportError:
                self.device = "cpu"
                logger.warning("PyTorch not installed in environment yet. Defaulting device to 'cpu'.")

    def load_model(self) -> None:
        """
        Lazy loads tokenizer and pretrained PyTorch model into memory.
        Downloads model files on first invocation.
        """
        self._init_device()

        if self.model is None or self.tokenizer is None:
            logger.info(f"Loading tokenizer and model '{self.model_name}' (Cache directory: {self.cache_dir})...")
            os.makedirs(self.cache_dir, exist_ok=True)

            try:
                import torch
                from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

                self.tokenizer = M2M100Tokenizer.from_pretrained(
                    self.model_name, cache_dir=self.cache_dir
                )
                self.model = M2M100ForConditionalGeneration.from_pretrained(
                    self.model_name, cache_dir=self.cache_dir
                ).to(self.device)
                
                # Set evaluation mode for inference
                self.model.eval()
                logger.info("Model and tokenizer loaded successfully.")
            except ImportError as ie:
                logger.error(f"Missing required ML libraries: {ie}")
                raise RuntimeError(
                    "PyTorch or Transformers library is missing. "
                    "Please run 'pip install -r requirements.txt' in your virtual environment."
                ) from ie
            except Exception as e:
                logger.error(f"Failed to load model weights for '{self.model_name}': {e}")
                raise RuntimeError(
                    f"Could not load neural translation model ({self.model_name}). "
                    "Ensure internet access for initial download or verify package installation."
                ) from e

    def translate(self, text: str, src_lang: str = "auto", tgt_lang: str = "en") -> Dict[str, Any]:
        """
        Translates text from source language to target language using PyTorch neural inference.

        Args:
            text (str): Input text string.
            src_lang (str): Source language code ('auto' or ISO code like 'hi', 'ta', 'en').
            tgt_lang (str): Target language code ('en', 'hi', 'ta', etc.).

        Returns:
            dict: {
                "translation": str,
                "src_lang": str,
                "detected_lang": Optional[str],
                "tgt_lang": str
            }
        """
        if not text or not text.strip():
            raise ValueError("Input text for translation cannot be empty.")

        if tgt_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Target language '{tgt_lang}' is not supported. Supported languages: {list(SUPPORTED_LANGUAGES.keys())}"
            )

        detected_lang = None

        # Auto-detect language if requested or unspecified
        if src_lang == "auto" or not src_lang:
            detected_lang = self.detector.detect_language(text)
            src_lang = detected_lang
            logger.info(f"Auto-detected source language: {detected_lang} ('{SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown')}')")
        elif src_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Source language '{src_lang}' is not supported. Supported languages: {list(SUPPORTED_LANGUAGES.keys())}"
            )

        # Ensure model is initialized
        self.load_model()

        try:
            import torch

            # Configure tokenizer for source language
            self.tokenizer.src_lang = src_lang

            # Tokenize input string
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

            # Get target language token ID
            forced_bos_token_id = self.tokenizer.get_lang_id(tgt_lang)

            # Perform neural machine translation inference using PyTorch
            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=forced_bos_token_id,
                    max_length=512
                )

            # Decode generated tokens back to text string
            translated_text = self.tokenizer.batch_decode(
                generated_tokens, skip_special_tokens=True
            )[0]

            return {
                "translation": translated_text,
                "src_lang": src_lang,
                "detected_lang": detected_lang,
                "tgt_lang": tgt_lang
            }

        except Exception as e:
            logger.error(f"Inference error during translation ({src_lang} -> {tgt_lang}): {e}")
            raise RuntimeError(f"Translation inference failed: {str(e)}") from e
