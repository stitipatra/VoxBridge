# VoxBridge

> **Offline Multilingual Translation for Text, Audio, and Video with AI-generated Speech & Subtitles**

VoxBridge is an end-to-end offline translation system that translates **text, audio, and video** between multiple languages while preserving accessibility through **speech synthesis** and **subtitle generation**. Unlike cloud-based translators, VoxBridge performs the complete pipeline locally without requiring internet connectivity or external APIs.

---

## ✨ Features

* 🌍 Offline multilingual translation
* 🎥 Video translation with burned-in subtitles
* 🎵 Audio translation with AI-generated speech
* 📄 Text translation with speech generation
* 📝 Automatic subtitle (.srt) generation
* 🎙️ Automatic speech recognition
* 🔊 Male/Female voice selection
* 🚀 Fully local processing (No API Keys)
* 🔒 Privacy-first architecture

---

## Supported Languages

| Language | Code |
| -------- | ---- |
| English  | en   |
| Hindi    | hi   |
| Marathi  | mr   |

---

## AI Stack

| Component           | Technology     |
| ------------------- | -------------- |
| Speech Recognition  | Faster-Whisper |
| Machine Translation | NLLB-200       |
| Speech Synthesis    | eSpeak NG      |
| Video Processing    | FFmpeg         |
| Backend             | FastAPI        |
| Frontend            | Streamlit      |

---

## Processing Pipeline

```
Input
(Text / Audio / Video)
        │
        ▼
Speech Recognition (Whisper)
        │
        ▼
Language Detection
        │
        ▼
Translation (NLLB)
        │
        ▼
Subtitle Generation
        │
        ▼
Speech Generation
        │
        ▼
Video Rendering (FFmpeg)
        │
        ▼
Translated Output
```

---

## Project Structure

```
VoxBridge
│
├── app/
│   ├── ai/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── config.py
│   └── main.py
│
├── models/
│
├── storage/
│
├── tools/
│   ├── espeak/
│   └── ffmpeg/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/VoxBridge.git

cd VoxBridge
```

Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

---

## Running the Frontend

In another terminal

```bash
streamlit run streamlit_app.py
```

Frontend opens automatically at

```
http://localhost:8501
```

---

## Supported Inputs

### Text

```
.txt
```

### Audio

```
.mp3
.wav
.m4a
.aac
.flac
```

### Video

```
.mp4
.mov
.mkv
.avi
```

---

## Outputs

Depending on the input type, VoxBridge generates:

* Translated Text
* AI-generated Speech (.wav)
* Original Transcript
* Original Subtitles (.srt)
* Translated Subtitles (.srt)
* Final Translated Video (.mp4)

---

## Highlights

* ✅ 100% Offline
* ✅ No Cloud APIs
* ✅ No API Keys
* ✅ Privacy Focused
* ✅ Local AI Processing

---

## Demo Workflow

1. Upload a Text, Audio, or Video file.
2. Select source language (or Auto Detect).
3. Select target language.
4. Choose Male or Female voice.
5. Click **Translate Now**.
6. Download translated outputs.

---

## Future Enhancements

* Additional language support
* Neural TTS voices
* Speaker diarization
* Lip-sync preservation
* GPU acceleration
* Batch processing
* Real-time streaming translation

---

## Authors

**Stitiprangya Patra**

BITS Pilani Goa Campus

---

## License

This project is intended for educational and research purposes.
