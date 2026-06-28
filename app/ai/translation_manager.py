from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

_tokenizer = None
_model = None


def get_translation_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("Loading translation model...")

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

        print("Translation model loaded.")

    return _tokenizer, _model
