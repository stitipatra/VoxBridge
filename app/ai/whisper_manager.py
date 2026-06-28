from faster_whisper import WhisperModel

_whisper_model = None


def get_whisper_model():
    global _whisper_model

    if _whisper_model is None:
        _whisper_model = WhisperModel(
            "medium",
            device="cpu",
            compute_type="int8"
        )

    return _whisper_model
