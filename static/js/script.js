/**
 * BharatTranslate AI - Frontend Controller Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const srcLangSelect = document.getElementById('srcLangSelect');
    const tgtLangSelect = document.getElementById('tgtLangSelect');
    const swapLangsBtn = document.getElementById('swapLangsBtn');
    const srcTextInput = document.getElementById('srcTextInput');
    const tgtTextOutput = document.getElementById('tgtTextOutput');
    const translateBtn = document.getElementById('translateBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const copyBtnText = document.getElementById('copyBtnText');
    const charCount = document.getElementById('charCount');
    const detectedBadge = document.getElementById('detectedBadge');
    const detectedLangName = document.getElementById('detectedLangName');
    const errorBanner = document.getElementById('errorBanner');
    const errorMessage = document.getElementById('errorMessage');
    const closeErrorBtn = document.getElementById('closeErrorBtn');
    const toast = document.getElementById('toast');

    // Update character counter as user types
    srcTextInput.addEventListener('input', () => {
        charCount.textContent = srcTextInput.value.length;
    });

    // Keyboard shortcut: Ctrl + Enter or Cmd + Enter to translate
    srcTextInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            performTranslation();
        }
    });

    // Clear input & output fields
    clearBtn.addEventListener('click', () => {
        srcTextInput.value = '';
        tgtTextOutput.textContent = '';
        charCount.textContent = '0';
        hideDetectedBadge();
        hideError();
    });

    // Swap Source and Target Languages
    swapLangsBtn.addEventListener('click', () => {
        const currentSrc = srcLangSelect.value;
        const currentTgt = tgtLangSelect.value;

        // If source is 'auto', don't swap to invalid target
        if (currentSrc === 'auto') {
            showToast("Cannot set target language to 'Auto Detect'");
            return;
        }

        srcLangSelect.value = currentTgt;
        tgtLangSelect.value = currentSrc;

        // Swap text contents if target text exists
        const currentOutput = tgtTextOutput.textContent;
        if (currentOutput.trim()) {
            srcTextInput.value = currentOutput;
            tgtTextOutput.textContent = '';
            charCount.textContent = currentOutput.length;
        }
    });

    // Copy Translation Result to Clipboard
    copyBtn.addEventListener('click', async () => {
        const textToCopy = tgtTextOutput.textContent.trim();
        if (!textToCopy) {
            showToast("Nothing to copy!");
            return;
        }

        try {
            await navigator.clipboard.writeText(textToCopy);
            copyBtnText.textContent = "Copied!";
            showToast("Translation copied to clipboard!");
            setTimeout(() => {
                copyBtnText.textContent = "Copy";
            }, 2000);
        } catch (err) {
            showToast("Failed to copy text");
        }
    });

    // Close Error Banner
    closeErrorBtn.addEventListener('click', hideError);

    // Translate Button Click Handler
    translateBtn.addEventListener('click', performTranslation);

    /**
     * Executes the translation process via API POST request.
     */
    async function performTranslation() {
        const text = srcTextInput.value.trim();
        const srcLang = srcLangSelect.value;
        const tgtLang = tgtLangSelect.value;

        if (!text) {
            showError("Please enter text to translate.");
            return;
        }

        hideError();
        setLoading(true);

        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    src_lang: srcLang,
                    tgt_lang: tgtLang
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Translation request failed.");
            }

            // Display translation output
            tgtTextOutput.textContent = data.translation;

            // Handle auto-detect badge
            if (srcLang === 'auto' && data.detected_lang_name) {
                showDetectedBadge(data.detected_lang_name);
            } else {
                hideDetectedBadge();
            }

        } catch (err) {
            showError(err.message || "Could not connect to translation server.");
        } finally {
            setLoading(false);
        }
    }

    // Helper UI functions
    function setLoading(isLoading) {
        if (isLoading) {
            translateBtn.disabled = true;
            btnText.textContent = "Translating...";
            btnSpinner.classList.remove('hidden');
        } else {
            translateBtn.disabled = false;
            btnText.textContent = "Translate";
            btnSpinner.classList.add('hidden');
        }
    }

    function showDetectedBadge(langName) {
        detectedLangName.textContent = langName;
        detectedBadge.classList.remove('hidden');
    }

    function hideDetectedBadge() {
        detectedBadge.classList.add('hidden');
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorBanner.classList.remove('hidden');
    }

    function hideError() {
        errorBanner.classList.add('hidden');
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 2500);
    }
});
