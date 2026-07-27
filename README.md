<div align="center">

# अनुवादिनी

### Breaking Language Barriers with Offline AI

**An AI-powered Offline Multimodal Translation Platform**

Translate **Text • Audio • Video** while automatically generating transcripts, subtitles, synchronized speech, and translated media — **completely offline**.

---

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![PyTorch](https://img.shields.io/badge/Framework-PyTorch-orange)
![Transformers](https://img.shields.io/badge/Translation-NLLB--200-yellow)
![Whisper](https://img.shields.io/badge/ASR-Faster--Whisper-blueviolet)
![Offline](https://img.shields.io/badge/Mode-100%25_Offline-success)

</div>

---

# Overview

**Anuwadini** is an AI-powered offline multimodal translation platform designed to break language barriers across **text, speech, and video**.

The platform automatically performs:

- Speech Recognition (ASR)
- Neural Machine Translation
- Subtitle Generation
- AI Voice Synthesis (TTS)
- Audio Synchronization
- Final Video Rendering

Unlike cloud-based translation services, every stage of the pipeline executes **locally on the user's machine**, ensuring complete privacy, zero recurring API costs, and multilingual accessibility.

Built using **Faster-Whisper**, **Meta NLLB-200**, **FFmpeg**, **FastAPI**, and **Streamlit**, Anuwadini provides an end-to-end translation workflow capable of processing multilingual media while remaining fully offline.

---

> **Privacy First. Offline by Design. Built for Multilingual Communication.**

# ✨ Features

## 🤖 AI Capabilities

- 🌍 Multilingual translation across **Text, Audio, and Video**
- 🎙️ Automatic Speech Recognition using **Faster-Whisper**
- 🌐 Neural Machine Translation powered by **Meta NLLB-200**
- 🗣️ Offline Text-to-Speech (TTS) synthesis
- 📝 Automatic subtitle generation with timestamp alignment
- 🔍 Automatic source language detection
- 🎯 Neural machine translation using Meta NLLB-200

---

## 🎥 Media Processing

- 📹 Video translation with translated speech
- 🎵 Audio translation with regenerated voice output
- 📄 Text translation across supported languages
- 🎬 Automatic subtitle burn-in
- 🎨 Styled ASS subtitle generation
- 🔄 Audio-video synchronization after speech generation
- 🎞️ Final translated media rendering using FFmpeg

---

## ⚡ Performance & Engineering

- 💻 Runs **100% offline** — no internet required
- 🔒 Privacy-first processing with no cloud uploads
- 📦 Supports media files up to **2 GB**
- 🚀 Modular translation pipeline designed for future performance optimizations
- 🧩 Modular architecture for independent pipeline stages
- 🔁 Retry-safe and resumable processing workflow

---

## 💻 User Experience

- 🖥️ Interactive Streamlit interface
- 📂 Simple upload-based workflow
- 📈 Real-time processing progress updates
- 📥 Download translated videos, audio, subtitles, and transcripts
- 🎯 Clean and intuitive user interface

# 🎬 Demo

## End-to-End Walkthrough

<p align="center">
  <video src="assets/walkthrough.mp4" controls width="90%">
    Your browser does not support the video tag.
  </video>
</p>

> **Complete walkthrough of Anuwadini showcasing text, audio, and video translation, subtitle generation, speech synthesis, and final translated media output.**

---

## Translation Pipeline

```text
                Input
                  │
      ┌───────────┼───────────┐
      │           │           │
    Text        Audio       Video
      │           │           │
      └───────────┼───────────┘
                  │
                  ▼
      Automatic Language Detection
                  │
                  ▼
      Speech Recognition (ASR)
                  │
                  ▼
      Neural Machine Translation
                  │
                  ▼
     Subtitle Generation (.SRT / .ASS)
                  │
                  ▼
      Offline Text-to-Speech (TTS)
                  │
                  ▼
        Audio Synchronization
                  │
                  ▼
        Final Media Rendering
                  │
                  ▼
      Translated Text • Audio • Video
```

---

## Generated Outputs

Every translation request automatically produces:

- 🎥 Translated Video
- 🎵 Translated Audio
- 📝 Speech Transcript
- 💬 Subtitle Files (`.srt` / `.ass`)
- 🌍 Translated Text
- 📦 Ready-to-download output files

# 🏗️ System Architecture

Anuwadini follows a modular pipeline architecture where each processing stage is isolated into independent components. This design improves maintainability, extensibility, and allows individual stages to be optimized without affecting the rest of the workflow.

> **Architecture Diagram** _(Replace with the final diagram later)_

```text
                           User Input
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
       Text                  Audio                  Video
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                                ▼
                     Language Detection
                                │
                                ▼
                   Faster-Whisper (ASR)
                                │
                                ▼
                Meta NLLB-200 Translation
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
              ▼                                   ▼
      Subtitle Generation                Text Output
              │
              ▼
      Offline Text-to-Speech
              │
              ▼
      Audio Synchronization
              │
              ▼
      FFmpeg Video Rendering
              │
              ▼
           Final Outputs
```

---

## Design Principles

The architecture was built around the following engineering principles:

- **Modularity** – Each processing stage is implemented as an independent service.
- **Offline First** – No cloud APIs or internet connectivity required during translation.
- **Privacy by Design** – User media never leaves the local machine.
- **Extensibility** – Individual models or pipeline stages can be replaced without redesigning the application.
- **Scalability** – The workflow supports large media files while maintaining a structured processing pipeline.

# ⚙️ Technology Stack

| Category                     | Technology                | Purpose                                                |
| ---------------------------- | ------------------------- | ------------------------------------------------------ |
| **Frontend**                 | Streamlit                 | Interactive web interface for translation workflow     |
| **Backend API**              | FastAPI                   | Modular backend services and request handling          |
| **Speech Recognition (ASR)** | Faster-Whisper            | High-performance multilingual speech-to-text           |
| **Translation**              | Meta NLLB-200             | Offline neural machine translation                     |
| **Speech Synthesis (TTS)**   | Piper TTS                 | Offline multilingual voice generation                  |
| **Media Processing**         | FFmpeg                    | Audio extraction, synchronization, and video rendering |
| **Deep Learning Framework**  | PyTorch                   | Model inference and execution                          |
| **Machine Learning**         | Hugging Face Transformers | Loading and running NLLB translation models            |
| **Subtitle Processing**      | SRT / ASS                 | Subtitle generation and styling                        |
| **Programming Language**     | Python                    | Core application development                           |

---

# 🧠 Why These Technologies?

### 🎙️ Faster-Whisper

Chosen for fast, accurate, and fully offline multilingual speech recognition with significantly lower inference time compared to the original Whisper implementation.

---

### 🌍 Meta NLLB-200

Provides high-quality neural machine translation across hundreds of languages while running entirely offline, eliminating dependency on cloud translation services.

---

### 🗣️ Piper TTS

Generates natural-sounding speech locally without requiring external APIs, ensuring user privacy and offline accessibility.

---

### 🎬 FFmpeg

Handles media processing tasks including:

- Audio extraction
- Subtitle embedding
- Audio replacement
- Video rendering
- Media synchronization

---

### ⚡ FastAPI

Provides a modular backend architecture, allowing each stage of the translation pipeline to remain independent and easily extensible.

---

### 🖥️ Streamlit

Offers a lightweight and interactive interface that enables users to upload files, configure translations, monitor progress, and download generated outputs with minimal setup.

# 📂 Repository Structure

```text
Anuwadini/
│
├── app.py                  # Streamlit application entry point
├── process.py              # End-to-end translation pipeline
├── requirements.txt
├── README.md
│
├── assets/                 # Images, demo GIFs, walkthrough videos
│   ├── walkthrough.mp4
│   ├── home.png
│   └── ...
│
├── services/
│   ├── transcription_service.py
│   ├── translation_service.py
│   ├── tts_service.py
│   ├── subtitle_service.py
│   └── ...
│
├── managers/
│   ├── whisper_manager.py
│   ├── translation_manager.py
│   └── ...
│
├── utils/
│   ├── file_utils.py
│   ├── language_utils.py
│   └── ...
│
├── outputs/                # Generated outputs
│   ├── translated_video.mp4
│   ├── translated_audio.wav
│   ├── subtitles.srt
│   ├── subtitles.ass
│   └── transcript.txt
│
├── uploads/                # Temporary uploaded media
│
└── file_changes/           # Experimental implementations preserved for future development
```

---

## Directory Overview

| Directory         | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| **assets/**       | Images, walkthrough videos, logos, and documentation resources              |
| **services/**     | Core AI services such as ASR, translation, subtitle generation, and TTS     |
| **managers/**     | Model loading, initialization, and lifecycle management                     |
| **utils/**        | Helper utilities shared across the application                              |
| **outputs/**      | Generated translated media and supporting files                             |
| **uploads/**      | Temporary storage for user-uploaded media                                   |
| **file_changes/** | Experimental implementations preserved for future optimization and research |

# 🚀 Installation

## Prerequisites

Before getting started, ensure you have the following installed:

- Python **3.10 or later** (Recommended: Python 3.12)
- Git
- FFmpeg (added to system PATH)
- pip

---

## 1. Clone the Repository

```bash
git clone https://github.com/stitipatra/Anuwadini.git
cd Anuwadini
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Install FFmpeg

Anuwadini uses **FFmpeg** for audio extraction, synchronization, subtitle embedding, and final video rendering.

### Windows

1. Download FFmpeg.
2. Extract the archive.
3. Add the `bin` directory to your system `PATH`.

Verify the installation:

```bash
ffmpeg -version
```

---

## 5. Launch the Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser.

---

# 🐍 Using an Older Python Version

If multiple Python versions are installed, create the virtual environment using the desired interpreter.

### Example (Python 3.10)

```bash
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Example (Python 3.11)

```bash
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Verify Installation

Run the following commands to verify your environment:

```bash
python --version
ffmpeg -version
streamlit --version
```

If all commands execute successfully, Anuwadini is ready to use.

# 📖 Usage

Anuwadini provides a simple workflow for translating **Text**, **Audio**, and **Video** while remaining completely offline.

---

## Step 1 — Launch the Application

```bash
streamlit run streamlit_app.py
```

Open the application in your browser.

---

## Step 2 — Upload Input

Choose one of the supported input types:

- 📄 Text
- 🎵 Audio
- 🎥 Video

Supported media formats include common audio and video file types.

---

## Step 3 — Configure Translation

Select:

- Source Language _(or Auto Detect)_
- Target Language
- Translation Mode

The application automatically configures the required processing pipeline.

---

## Step 4 — Start Translation

Click **Translate**.

The application performs the following stages automatically:

1. Language Detection
2. Speech Recognition (ASR)
3. Neural Machine Translation
4. Subtitle Generation
5. Speech Synthesis (TTS)
6. Audio Synchronization
7. Final Media Rendering

Real-time progress updates are displayed throughout the pipeline.

---

## Step 5 — Download Results

After processing completes, the generated outputs are available for download.

Depending on the input type, outputs include:

- 🎥 Translated Video
- 🎵 Translated Audio
- 📝 Transcript
- 💬 Subtitle Files (.srt / .ass)
- 🌍 Translated Text

---

# 🌍 Supported Languages

Current language support includes:

| Language | Text | Audio | Video |
| -------- | :--: | :---: | :---: |
| English  |  ✅  |  ✅   |  ✅   |
| Hindi    |  ✅  |  ✅   |  ✅   |
| Marathi  |  ✅  |  ✅   |  ✅   |

The modular architecture allows additional languages to be integrated with minimal changes.

---

# 📁 Supported Input Formats

### Video

- MP4
- AVI
- MOV
- MKV
- WEBM

### Audio

- WAV
- MP3
- M4A
- FLAC
- AAC

### Text

- Plain Text
- TXT Files

---

# 📤 Generated Outputs

For every successful translation, Anuwadini generates one or more of the following artifacts:

| Output              | Description                                         |
| ------------------- | --------------------------------------------------- |
| 🎥 Translated Video | Original video with translated speech and subtitles |
| 🎵 Translated Audio | Synthesized translated speech                       |
| 📝 Transcript       | Speech-to-text transcription                        |
| 💬 SRT Subtitle     | Standard subtitle format                            |
| 🎨 ASS Subtitle     | Styled subtitle format                              |
| 🌍 Translated Text  | Final translated text output                        |

# 📊 Performance

Performance was evaluated on CPU using long-form multilingual media to understand the execution time of each stage in the translation pipeline.

## Pipeline Execution Time

| Stage                      |          Execution Time |
| -------------------------- | ----------------------: |
| Audio Preparation          |                  ~0.6 s |
| Speech Recognition (ASR)   |                  ~369 s |
| Neural Machine Translation |                  ~560 s |
| Subtitle Generation        |                  ~0.4 s |
| Text-to-Speech (TTS)       |                  ~153 s |
| Audio Synchronization      |                  ~0.5 s |
| Video Rendering            |                   ~37 s |
| **Total Pipeline**         | **~1123 s (~18.7 min)** |

> **Note:** Performance varies depending on hardware specifications, media duration, selected languages, and model initialization.

---

## Current Performance Characteristics

- Fully offline execution
- No dependency on cloud APIs
- Modular processing pipeline
- Supports media files up to **2 GB**
- Optimized for reliability and translation quality over latency

---

## Future Optimization Opportunities

Several optimizations are planned for future releases, including:

- Batched translation for long-form media
- Parallel execution of independent pipeline stages
- GPU acceleration
- ONNX / TensorRT model optimization
- Dynamic translation chunk sizing
- Streaming translation for real-time processing

These improvements are expected to significantly reduce end-to-end execution time while maintaining translation quality.

# 💡 Engineering Decisions

Anuwadini was designed with three primary objectives:

1. **Complete Offline Operation**
2. **High Translation Quality**
3. **Modular and Extensible Architecture**

The following design decisions were made to achieve these goals.

---

## 🌐 Offline-First Architecture

Every stage of the pipeline executes locally on the user's machine.

Unlike cloud-based translation services, Anuwadini does not require:

- Internet connectivity
- External APIs
- API keys
- Subscription services

This ensures:

- Complete user privacy
- Zero recurring inference cost
- Reliable operation in low-connectivity environments

---

## 🎙️ Faster-Whisper for Speech Recognition

Faster-Whisper was selected because it provides:

- High multilingual transcription accuracy
- Significantly faster inference than the original Whisper implementation
- Efficient CPU execution
- Automatic language detection

It serves as the speech recognition backbone for audio and video inputs.

---

## 🌍 Meta NLLB-200 for Translation

Meta's NLLB-200 model was chosen to enable high-quality multilingual translation while remaining fully offline.

Reasons for selection include:

- Broad multilingual support
- Strong translation quality
- Local inference without cloud dependency
- Easy integration through Hugging Face Transformers

---

## 🗣️ Hybrid Offline Text-to-Speech

Different languages require different TTS capabilities.

Anuwadini combines multiple offline speech synthesis engines to provide the best available voice quality across supported languages.

This modular approach also allows future TTS engines to be integrated with minimal code changes.

---

## 🎬 FFmpeg-Based Media Processing

FFmpeg is used throughout the media pipeline for:

- Audio extraction
- Audio replacement
- Subtitle embedding
- Video rendering
- Media synchronization

Using FFmpeg enables compatibility with a wide range of multimedia formats while maintaining high output quality.

---

## 🧩 Modular Service-Oriented Design

The application is organized into independent services responsible for specific stages of the workflow.

Examples include:

- Speech Recognition
- Translation
- Text-to-Speech
- Subtitle Generation
- Media Processing

This separation of responsibilities improves maintainability, testing, and future extensibility.

---

## ⚖️ Translation Quality over Raw Speed

The current implementation prioritizes translation accuracy, consistency, and deterministic outputs over aggressive runtime optimization.

The architecture has been intentionally designed to support future performance improvements without requiring significant structural changes.

---

## 🔒 Privacy by Design

User files remain on the local machine throughout processing.

No audio, video, transcripts, or translated content are transmitted to external servers, making the platform suitable for privacy-sensitive translation workflows.

# 🚧 Engineering Challenges

Building an end-to-end offline multilingual translation platform involved solving several engineering challenges across speech recognition, translation, media processing, and user experience.

---

## 🎙️ Accurate Speech Recognition

Speech recognition quality directly impacts the quality of translation and speech synthesis.

Challenges included:

- Multiple accents and speaking styles
- Background noise
- Mixed-language speech
- Long-duration media processing

The pipeline was designed to produce reliable transcriptions while remaining fully offline.

---

## 🌍 Multilingual Translation

Supporting multiple languages required selecting a translation model capable of balancing quality, inference speed, and offline execution.

The translation component was designed as an independent module, allowing future improvements or alternative models to be integrated with minimal architectural changes.

---

## 💬 Subtitle Generation

Generating subtitles involves more than translating text.

The system needed to ensure:

- Accurate timestamp alignment
- Readable subtitle segmentation
- Proper multilingual font rendering
- Compatibility with multiple subtitle formats

Support for both **SRT** and **ASS** subtitles provides flexibility for different playback environments.

---

## 🔊 Speech Synthesis

Natural speech generation required balancing voice quality with execution speed.

Different languages may require different synthesis approaches, so the TTS layer was designed to be modular and easily extensible.

---

## 🎬 Media Synchronization

Translated speech often differs in duration from the original audio.

Maintaining synchronization between translated speech, subtitles, and video required careful handling of media timelines before final rendering.

---

## 💻 Fully Offline Execution

One of the primary goals of Anuwadini was complete offline operation.

This required replacing cloud services with local AI models while ensuring that transcription, translation, speech synthesis, and media processing could execute entirely on the user's machine.

---

## 🧩 Modular Architecture

The application was intentionally divided into independent services for:

- Speech Recognition
- Translation
- Subtitle Generation
- Text-to-Speech
- Media Processing

This separation improves maintainability, testing, debugging, and future feature development.


# ⚠️ Known Limitations

While Anuwadini provides a complete offline multilingual translation workflow, there are several areas identified for future enhancement.

---

## 🎙️ Speech Recognition Accuracy

The quality of the final translation depends heavily on the accuracy of Automatic Speech Recognition (ASR).

Factors such as:

- Strong regional accents
- Background noise
- Rapid speech
- Code-switched conversations
- Low-quality recordings

may reduce transcription accuracy, which can propagate to later stages of the pipeline.

---

## 🌍 Translation Quality

Translation quality varies across language pairs and is influenced by the underlying multilingual translation model.

Some complex idioms, domain-specific terminology, or culturally nuanced expressions may not always be translated perfectly.

---

## 🗣️ Text-to-Speech Voices

Voice quality depends on the availability of offline TTS models for the selected language.

Current voices prioritize offline accessibility and functionality over highly expressive or human-like speech.

---

## ⏱️ Processing Time

As the entire pipeline executes locally without cloud acceleration, processing time increases with:

- Media duration
- Video resolution
- CPU capabilities
- Available system memory

Long-form videos therefore require noticeably longer execution times than short clips.

---

## 💻 Hardware Dependency

Inference performance depends on the user's hardware configuration.

Systems equipped with dedicated GPUs can potentially achieve significantly faster execution once GPU inference support is enabled.

---

## 📹 Supported Workflows

The current release focuses on offline batch translation of uploaded media.

Real-time translation, live streaming, and microphone-based translation are not yet supported.

# 🚀 Future Improvements

Anuwadini has been designed with extensibility in mind. The modular architecture enables new models, languages, and processing techniques to be integrated with minimal structural changes.

---

## ⚡ Performance Optimizations

Future work will focus on reducing end-to-end processing time while maintaining translation quality.

Planned improvements include:

- Batch translation for long-form media
- Parallel execution of independent pipeline stages
- GPU acceleration for ASR, Translation, and TTS
- Dynamic translation chunk sizing
- Intelligent caching of frequently used models
- Memory-efficient inference for large media files

---

## 🎙️ Speech Recognition

Future enhancements to the ASR pipeline include:

- Improved transcription accuracy for Marathi
- Better handling of code-switched multilingual conversations
- Benchmarking larger Whisper models
- Speaker diarization for multi-speaker conversations
- Adaptive decoding strategies for noisy environments

---

## 🌍 Translation

Planned translation improvements include:

- Context-aware translation across long conversations
- Translation memory for repeated phrases
- Domain-specific translation support
- Additional multilingual model benchmarking
- Improved consistency for long-form media

---

## 🗣️ Text-to-Speech

Future work on speech synthesis includes:

- More natural multilingual voices
- Speaker-aware voice generation
- Voice selection options
- Improved speech pacing and pronunciation
- Additional offline TTS model support

---

## 🎥 Media Processing

Upcoming enhancements include:

- Real-time subtitle preview
- Automatic subtitle styling options
- Improved subtitle segmentation
- Better synchronization between translated speech and video
- Batch processing of multiple media files

---

## 🌐 Language Support

Future releases aim to expand multilingual accessibility by supporting additional Indian and international languages while maintaining fully offline execution.

---

## 💻 User Experience

Planned interface improvements include:

- Drag-and-drop uploads
- Live progress estimation
- Translation history
- Project management dashboard
- User-configurable processing settings
- Dark mode

---

## 🔌 Platform Enhancements

Future versions may include:

- Docker support
- REST API
- Desktop application
- Cloud deployment option
- Plugin architecture
- Automated testing and CI/CD pipelines

# 🗺️ Project Roadmap

The roadmap below outlines the current capabilities of Anuwadini along with planned enhancements for future releases.

---

## ✅ Completed

### Core Platform

- Fully offline multilingual translation
- Text translation
- Audio translation
- Video translation
- Automatic language detection
- Automatic Speech Recognition (ASR)
- Neural Machine Translation
- Offline Text-to-Speech (TTS)
- Subtitle generation (SRT & ASS)
- Audio synchronization
- Final video rendering
- Interactive Streamlit interface

---

## 🚧 In Progress

Current areas of research and development include:

- Performance optimization for long-form media
- Improved multilingual speech recognition
- Enhanced subtitle quality
- More natural offline voice synthesis
- Pipeline optimization for reduced inference time

---

## 🔜 Planned

### Performance

- Batch translation for long-form media
- Parallel pipeline execution
- GPU acceleration
- Intelligent model caching

### Speech Recognition

- Improved Marathi transcription
- Better handling of multilingual conversations
- Speaker diarization
- Noise-robust transcription

### Translation

- Context-aware translation
- Translation memory
- Improved consistency across long conversations
- Additional multilingual model benchmarking

### Media Processing

- Better subtitle synchronization
- Improved subtitle segmentation
- Batch media processing
- Advanced subtitle styling

### User Experience

- Drag-and-drop uploads
- Translation history
- Progress estimation
- Configurable processing settings
- Desktop application

---

## 🌟 Long-Term Vision

The long-term goal of Anuwadini is to become a comprehensive **offline multilingual communication platform** capable of enabling seamless translation across text, speech, and video while preserving user privacy.

Future milestones include:

- Support for additional Indian and international languages
- Live microphone translation
- Real-time streaming translation
- REST API
- Docker deployment
- Plugin architecture
- Cross-platform desktop application

# 🤝 Contributing

Contributions, feature requests, and suggestions are welcome.

If you would like to improve Anuwadini, please follow these steps:

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add your feature"
```

4. Push the branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

Please ensure that new features maintain the project's offline-first philosophy and modular architecture.

---

# 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software in accordance with the terms of the license.

See the `LICENSE` file for more details.

---

# 🙏 Acknowledgements

This project builds upon several outstanding open-source technologies.

Special thanks to:

- Meta AI for **NLLB-200**
- Faster-Whisper for multilingual speech recognition
- Hugging Face Transformers
- PyTorch
- Piper TTS
- FFmpeg
- Streamlit
- FastAPI

Their contributions to the open-source community made this project possible.

---

# 👨‍💻 Author

**Stitiprangya Patra**

B.E. Electronics & Instrumentation Engineering + M.Sc. Mathematics  
BITS Pilani, Goa Campus

Software Engineer @ Nielsen

### Connect with Me

- GitHub: https://github.com/stitipatra
- LinkedIn: https://www.linkedin.com/in/stitipatra/
- Email: stitipatra@gmail.com

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star!

Thank you for visiting the repository.

**Breaking Language Barriers with Offline AI.**

</div>