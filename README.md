# अनुवादिनी

> **Offline Multilingual Translation for Text, Audio, and Video with AI-generated Speech & Subtitles**

अनुवादिनी is an end-to-end offline AI-powered translation system that translates **text, audio, and video** into multiple languages while preserving accessibility through **speech synthesis** and **subtitle generation**. All processing is performed locally without requiring cloud services or API keys.

---

## Demo

![अनुवादिनी Demo](walkthrough/demo.gif)

---

# Features

- 🌍 Offline multilingual translation
- 🎥 Video translation with embedded subtitles
- 🎵 Audio translation with AI-generated speech
- 📄 Text translation with speech generation
- 📝 Automatic subtitle (.srt) generation
- 🎙️ Automatic speech recognition
- 🔊 Male/Female voice selection
- 🔒 Privacy-first local processing
- 🚀 No internet or API keys required

* 🖥️ Fully Offline AI Inference
* 📱 Portrait & Landscape Subtitle Support
* 🎨 Dynamic ASS Subtitle Rendering
* 📦 Supports media uploads up to 2 GB

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

# Design Decisions

अनुवादिनी prioritizes **translation quality**, **offline execution**, and **subtitle consistency** over aggressive parallel processing.

### Full-Context Translation

Instead of translating each Whisper segment independently, अनुवादिनी first generates a complete transcript and translates it as a single document.

This approach:

- Produces more natural translations.
- Preserves sentence-level context.
- Ensures the translated text shown in the UI exactly matches the embedded subtitles.
- Simplifies debugging and deterministic processing.

### Audio Synchronization

Languages differ in speaking speed and sentence structure.

To preserve speech quality:

- Small duration differences are automatically corrected.
- Large differences are adjusted only within a safe playback-speed boundary.
- Excessive slow-motion speech is intentionally avoided.
- Video duration is always preserved and subtitles continue throughout the entire video.

### Offline First

The complete pipeline runs locally using Faster-Whisper, NLLB-200, eSpeak NG and FFmpeg.

No cloud APIs, internet connection, or API keys are required after setup.

---

# Project Structure

```text
अनुवादिनी
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
git clone https://github.com/<your-username>/अनुवादिनी.git

cd अनुवादिनी
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

# Running अनुवादिनी

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

# Scalability

Although the current implementation processes media using a single translation pipeline, the architecture has been intentionally designed to support future scaling.

Potential enhancements include:

- Chunk-based transcription for long videos
- Parallel Whisper inference
- Queue-based worker processing
- GPU-backed batch inference
- Segment-level TTS alignment
- Distributed media storage
- REST API deployment using FastAPI
- Real-time progress tracking

---

# Supported Inputs

### Text

- `.txt`

### Audio

- `.mp3`
- `.wav`
- `.m4a`
- `.aac`
- `.flac`

### Video

- `.mp4`
- `.mov`
- `.mkv`
- `.avi`

---

# Generated Outputs

Depending on the input type, अनुवादिनी produces:

- 📄 Translated Text
- 🎙️ Transcript
- 🌍 Translation
- 🔊 AI-generated Speech
- 📝 Original Subtitles (.srt)
- 📝 Translated Subtitles (.srt)
- 🎥 Final Translated Video

---

# Edge Cases Handled

- GPU unavailable → automatic CPU fallback
- Portrait and landscape subtitle rendering
- Cross-platform bundled FFmpeg and eSpeak support
- Large media uploads (up to 2 GB)
- Multiple video and audio formats
- Dynamic subtitle scaling
- Automatic language detection
- Graceful handling of unsupported files

---

# Highlights

- ✅ Fully Offline
- ✅ Privacy First
- ✅ No API Keys
- ✅ Local AI Processing
- ✅ Cross-format Translation
- ✅ Automatic Subtitle Generation

---

# Engineering Challenges & Solutions

| Challenge                            | Solution                                                                      |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| Incorrect Hindi subtitle rendering   | Migrated from SRT to ASS subtitles with bundled Noto Sans Devanagari font     |
| Subtitle overflow on portrait videos | Dynamic font sizing, margins and language-specific wrapping                   |
| Translation inconsistencies          | Adopted full-context translation instead of segment-wise translation          |
| Audio/video duration mismatch        | Implemented bounded playback-speed adjustment while preserving speech quality |
| Cross-platform deployment            | Bundled FFmpeg, fonts and eSpeak dependencies                                 |
| Large file uploads                   | Increased Streamlit upload limit to support media files up to 2 GB            |

---

# Future Enhancements

- Additional language support
- Neural TTS voices (Piper / Coqui)
- Segment-level TTS synchronization
- Chunk-based transcription for very large videos
- Parallel inference pipelines
- Speaker diarization
- Voice cloning
- Lip-sync alignment
- Batch translation
- GPU optimization
- REST API deployment
- Real-time translation

---

# Performance Characteristics

- Fully offline inference
- Runtime API cost: **₹0 / $0**
- Modular service-oriented architecture
- Supports text, audio and video translation
- Supports English, Hindi and Marathi
- Upload size up to **2 GB**
- Cross-platform compatible (Windows, macOS and Linux)

---

# Author

**Stitiprangya Patra**

BITS Pilani Goa Campus

---

# License

This project is intended for educational and research purposes.
