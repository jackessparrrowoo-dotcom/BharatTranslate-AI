# BharatTranslate AI 🇮🇳

**BharatTranslate AI** is a professional, open-source Indian language neural translation web application powered by **Python**, **PyTorch**, **Hugging Face Transformers (`facebook/m2m100_418M`)**, and **Flask**.

It provides high-accuracy, deep-learning powered translation across 10 major Indian and international languages with automatic language detection, a responsive modern web UI, and clean modular code architecture.

---

## 🌟 Features

- 🧠 **True Deep Learning NLP**: Uses Hugging Face's `M2M100` sequence-to-sequence multilingual model.
- ⚡ **Auto Language Detection**: Hybrid engine matching Indian Unicode scripts (Devanagari, Tamil, Telugu, Malayalam, Kannada, Bengali, Gujarati, Gurmukhi) with statistical language detection fallback.
- 🎨 **Modern Responsive UI**: Clean interface built with HTML5, CSS3, and JavaScript featuring character counters, swap languages, copy to clipboard, and status indicators.
- 🧩 **Modular Architecture**: Separate translation core, language detection engine, and Flask server routes.
- 🚀 **Hardware Acceleration**: Automatic GPU (`cuda`) detection with seamless CPU fallback.

---

## 🌐 Supported Languages

| Language | ISO Code | Language | ISO Code |
|---|---|---|---|
| **English** | `en` | **Bengali** | `bn` |
| **Hindi** | `hi` | **Marathi** | `mr` |
| **Tamil** | `ta` | **Gujarati** | `gu` |
| **Telugu** | `te` | **Punjabi** | `pa` |
| **Malayalam**| `ml` | **Kannada** | `kn` |

---

## 📁 Project Structure

```
BharatTranslate-AI/
├── app.py                     # Flask web server & REST API endpoints
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation & setup instructions
├── .gitignore                 # Git ignore patterns for ML models & Python
├── models/                    # Directory for cached PyTorch model weights
├── translation/               # Deep learning core package
│   ├── __init__.py
│   ├── translator.py          # Hugging Face M2M100 & PyTorch wrapper class
│   └── language_detector.py   # Hybrid language detector module
├── templates/
│   └── index.html             # Flask HTML UI template
├── static/
│   ├── css/
│   │   └── style.css          # Responsive CSS styles
│   └── js/
│       └── script.js          # Asynchronous frontend controller script
├── data/                      # Data storage directory
└── tests/
    ├── __init__.py
    └── test_translator.py     # Unit test suite
```

---

## 🛠️ Installation & Setup (Windows PowerShell)

Follow these step-by-step instructions to run BharatTranslate AI on your Windows machine:

### 1. Open PowerShell & Navigate to Project Directory
```powershell
cd D:\BharatTranslate-AI
```

### 2. Create & Activate a Python Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell blocks script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 Running the Web Application

### Start the Flask Server
```powershell
python app.py
```

Upon launching, open your browser and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

*Note: On your very first translation request, PyTorch will automatically download the pretrained `facebook/m2m100_418M` model weights (~1.6 GB) to the `models/` cache folder. Subsequent requests will load instantly from disk.*

---

## 🧪 Running Unit Tests

To run the automated unit test suite:

```powershell
python -m unittest discover -s tests
```
or with pytest:
```powershell
pytest
```

---

## 📡 API Endpoint Reference

### POST `/api/translate`
Translates text between supported languages.

**Request Body (JSON):**
```json
{
  "text": "வணக்கம் உலகம்",
  "src_lang": "auto",
  "tgt_lang": "en"
}
```

**Response (JSON):**
```json
{
  "success": true,
  "translation": "Hello world",
  "src_lang": "ta",
  "detected_lang": "ta",
  "detected_lang_name": "Tamil",
  "tgt_lang": "en"
}
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
