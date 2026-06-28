from pathlib import Path
import wave

from piper.voice import PiperVoice

model_path = "models/piper/hi_IN-pratham-medium.onnx"
output_path = "storage/audio_output/test_hindi.wav"

text = "नमस्कार सभी"

voice = PiperVoice.load(model_path)

with wave.open(output_path, "wb") as wav_file:
    voice.synthesize(text, wav_file)

print("saved:", output_path)
