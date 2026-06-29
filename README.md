# VoxBridge

> **Offline Multilingual Translation for Text, Audio, and Video with AI-generated Speech & Subtitles**

VoxBridge is an end-to-end offline AI-powered translation system that translates **text, audio, and video** into multiple languages while preserving accessibility through **speech synthesis** and **subtitle generation**. All processing is performed locally without requiring cloud services or API keys.

---

# Features

* 🌍 Offline multilingual translation
* 🎥 Video translation with embedded subtitles
* 🎵 Audio translation with AI-generated speech
* 📄 Text translation with speech generation
* 📝 Automatic subtitle (.srt) generation
* 🎙️ Automatic speech recognition
* 🔊 Male/Female voice selection
* 🔒 Privacy-first local processing
* 🚀 No internet or API keys required

---

# Supported Languages

| Language | Code |
| -------- | ---- |
| English  | en   |
| Hindi    | hi   |
| Marathi  | mr   |

---

# Technology Stack

| Module               | Technology     |
| -------------------- | -------------- |
| Speech Recognition   | Faster-Whisper |
| Translation          | NLLB-200       |
| Speech Synthesis     | eSpeak NG      |
| Video Processing     | FFmpeg         |
| Backend Architecture | FastAPI        |
| User Interface       | Streamlit      |

---

# Processing Pipeline

```text
Input (Text / Audio / Video)
        │
        ▼
Speech Recognition (Faster-Whisper)
        │
        ▼
Language Detection
        │
        ▼
Translation (NLLB-200)
        │
        ▼
Subtitle Generation
        │
        ▼
Speech Synthesis (eSpeak NG)
        │
        ▼
Video Rendering (FFmpeg)
        │
        ▼
Translated Output
```

---

# Project Structure

```text
VoxBridge
│
├── app/
│   ├── ai/
│   ├── routes/
│   ├── services/
│   ├── config.py
│   └── main.py
│
├── models/
├── storage/
├── tools/
│   ├── espeak/
│   └── ffmpeg/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# Installation

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

# Running VoxBridge

Launch the application

```bash
streamlit run streamlit_app.py
```

The Streamlit interface will open automatically in your browser.

---

# Architecture

Although the project is structured using **FastAPI** modules, the Streamlit frontend directly invokes the backend processing functions. This keeps deployment simple while maintaining a clean and modular architecture.

The processing pipeline is:

```text
Streamlit UI
      │
      ▼
process_file()
      │
      ▼
Transcription Service
      │
      ▼
Translation Service
      │
      ▼
TTS Service
      │
      ▼
Video Service
      │
      ▼
Output Files
```

The FastAPI application is retained to support future REST API integration without changing the processing logic.

---

# Supported Inputs

### Text

* `.txt`

### Audio

* `.mp3`
* `.wav`
* `.m4a`
* `.aac`
* `.flac`

### Video

* `.mp4`
* `.mov`
* `.mkv`
* `.avi`

---

# Generated Outputs

Depending on the input type, VoxBridge produces:

* 📄 Translated Text
* 🎙️ Transcript
* 🌍 Translation
* 🔊 AI-generated Speech
* 📝 Original Subtitles (.srt)
* 📝 Translated Subtitles (.srt)
* 🎥 Final Translated Video

---

# Highlights

* ✅ Fully Offline
* ✅ Privacy First
* ✅ No API Keys
* ✅ Local AI Processing
* ✅ Cross-format Translation
* ✅ Automatic Subtitle Generation

---

# Future Enhancements

* Additional language support
* Neural TTS voices
* Speaker diarization
* Batch translation
* GPU optimization
* Real-time translation

---

# Author

**Stitiprangya Patra**

BITS Pilani Goa Campus

---

# License

This project is intended for educational and research purposes.
