import time
from pathlib import Path

import torch
from scipy.io.wavfile import write
from transformers import AutoTokenizer, VitsModel


MODEL_NAME = "facebook/mms-tts-mar"

OUTPUT_DIR = Path("tests/output")
OUTPUT_FILE = OUTPUT_DIR / "marathi_mms.wav"

TEXT = (
    "नमस्कार सर्वांना हा व्हॉक्सब्रिजचा चाचणी व्हिडिओ आहे "
    "आज आपण इंग्रजी भाषेतील व्हिडिओ मराठीमध्ये भाषांतरित करणार आहोत"
)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading model...")

    start = time.perf_counter()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = VitsModel.from_pretrained(MODEL_NAME)

    print(f"Loaded in {time.perf_counter()-start:.2f}s")

    inputs = tokenizer(TEXT, return_tensors="pt")

    start = time.perf_counter()

    with torch.inference_mode():
        waveform = model(**inputs).waveform.squeeze()

    generation_time = time.perf_counter() - start

    audio = waveform.cpu().numpy()

    write(
        OUTPUT_FILE,
        rate=model.config.sampling_rate,
        data=audio,
    )

    duration = len(audio) / model.config.sampling_rate

    print(f"Generation time : {generation_time:.2f}s")
    print(f"Audio duration  : {duration:.2f}s")
    print(f"RTF             : {generation_time/duration:.2f}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()