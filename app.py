"""
BharatTranslate AI - Flask Web Application Backend
"""

import logging
from flask import Flask, render_template, request, jsonify
from translation.translator import Translator
from translation.language_detector import SUPPORTED_LANGUAGES

# Setup application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BharatTranslate")

app = Flask(__name__)

# Initialize single instance of Translator service
translator_service = Translator()


@app.route("/")
def index():
    """Renders the main translation web application interface."""
    return render_template("index.html", languages=SUPPORTED_LANGUAGES)


@app.route("/api/languages", methods=["GET"])
def get_languages():
    """Returns list of supported language codes and human-readable names."""
    return jsonify({"languages": SUPPORTED_LANGUAGES})


@app.route("/api/translate", methods=["POST"])
def translate_text():
    """
    Translates input text between supported Indian languages and English.

    JSON Request Body:
    {
        "text": "Text to translate",
        "src_lang": "auto|en|hi|ta|...",
        "tgt_lang": "en|hi|ta|..."
    }
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid request payload. Expected JSON body."}), 400

        text = data.get("text", "").strip()
        src_lang = data.get("src_lang", "auto").strip().lower()
        tgt_lang = data.get("tgt_lang", "en").strip().lower()

        if not text:
            return jsonify({"error": "Input text cannot be empty."}), 400

        logger.info(f"Translation request: src='{src_lang}', tgt='{tgt_lang}', text_len={len(text)}")

        # Execute neural translation via deep-learning model wrapper
        result = translator_service.translate(text=text, src_lang=src_lang, tgt_lang=tgt_lang)

        return jsonify({
            "success": True,
            "translation": result["translation"],
            "src_lang": result["src_lang"],
            "detected_lang": result["detected_lang"],
            "detected_lang_name": SUPPORTED_LANGUAGES.get(result["detected_lang"]) if result["detected_lang"] else None,
            "tgt_lang": result["tgt_lang"]
        })

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400

    except RuntimeError as re:
        logger.error(f"Runtime engine error: {re}")
        return jsonify({"error": str(re)}), 500

    except Exception as e:
        logger.error(f"Unexpected server error: {e}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred during translation."}), 500


if __name__ == "__main__":
    logger.info("Starting BharatTranslate AI Flask application...")
    app.run(host="0.0.0.0", port=5000, debug=True)
