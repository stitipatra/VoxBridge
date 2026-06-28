import os

BASE_DIR = os.getcwd()

FFMPEG_PATH = os.path.join(BASE_DIR, "tools", "ffmpeg", "bin", "ffmpeg.exe")
FFPROBE_PATH = os.path.join(BASE_DIR, "tools", "ffmpeg", "bin", "ffprobe.exe")

STORAGE_DIR = os.path.join(BASE_DIR, "storage")
AUDIO_OUTPUT_DIR = os.path.join(STORAGE_DIR, "audio_output")

ESPEAK_PATH = os.path.join(BASE_DIR, "tools", "espeak", "espeak-ng.exe")
ESPEAK_DATA_PATH = os.path.join(BASE_DIR, "tools", "espeak", "espeak-ng-data")

os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
