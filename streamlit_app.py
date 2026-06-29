import os
import time
import streamlit as st
from app.routes.process import ProcessRequest, process_file

UPLOAD_DIRS = {
    "video": os.path.join("storage", "uploads", "video"),
    "audio": os.path.join("storage", "uploads", "audio"),
    "text": os.path.join("storage", "uploads", "text"),
}

for folder in UPLOAD_DIRS.values():
    os.makedirs(folder, exist_ok=True)


def detect_input_type(filename: str) -> str:
    ext = filename.lower().split(".")[-1]

    if ext in ["mp4", "mov", "mkv", "avi"]:
        return "video"
    if ext in ["mp3", "wav", "m4a", "aac", "flac"]:
        return "audio"
    if ext in ["txt"]:
        return "text"

    raise ValueError("Unsupported file type")


def save_uploaded_file(uploaded_file, input_type: str) -> str:
    file_path = os.path.join(UPLOAD_DIRS[input_type], uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def download_button(label: str, file_path: str, mime: str):
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as file:
            st.download_button(
                label,
                file,
                file_name=os.path.basename(file_path),
                mime=mime,
                use_container_width=True
            )


st.set_page_config(
    page_title="VoxBridge",
    page_icon="🌉",
    layout="wide"
)

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_uploaded_file_name" not in st.session_state:
    st.session_state.last_uploaded_file_name = None

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1e3a8a 0%, #0f172a 35%, #020617 100%);
        color: #f8fafc;
    }

    .block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 2rem;
    max-width: 1320px;
}

header[data-testid="stHeader"]{
    background: transparent !important;
    height:0px;
}

div[data-testid="stToolbar"]{
    display:none;
}

div[data-testid="stDecoration"]{
    display:none;
}

section.main{
    padding-top:0rem !important;
}

    h1, h2, h3, h4, h5, h6, p, label {
    color: #f8fafc !important;
}

    .hero-title {
        font-size: 58px;
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 18px;
        margin-bottom: 26px;
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 24px;
        padding: 26px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.32);
    }

    .mini-card {
        background: rgba(2, 6, 23, 0.58);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 18px;
        padding: 16px 18px;
        min-height: 92px;
    }

    .mini-label {
        color: #94a3b8 !important;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .mini-value {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 900;
        margin-top: 6px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 900;
        margin-top: 24px;
        margin-bottom: 10px;
        color: #f8fafc !important;
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 14px !important;
        font-size: 15px !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: #f8fafc !important;
        color: #0f172a !important;
        border-radius: 12px !important;
    }

    .stSelectbox span {
        color: #0f172a !important;
    }

    .stRadio label span {
        color: #e2e8f0 !important;
    }

    .stFileUploader section {
        background: rgba(248, 250, 252, 0.96) !important;
        border-radius: 16px !important;
        border: 1px dashed #60a5fa !important;
    }

    .stFileUploader section * {
        color: #0f172a !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        height: 48px !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    height: 48px !important;
    font-weight: 800 !important;
}

    .stDownloadButton button {
        background: rgba(15, 23, 42, 0.95) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 14px !important;
        height: 46px !important;
        font-weight: 800 !important;
    }

    .stDownloadButton button:hover {
        background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
        color: white !important;
        border: 1px solid transparent !important;
    }

    video {
        max-height: 520px !important;
        border-radius: 18px !important;
        background: #020617 !important;
        object-fit: contain !important;
    }

    .success-box {
        background: rgba(34, 197, 94, 0.13);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: #bbf7d0 !important;
        border-radius: 16px;
        padding: 14px 18px;
        font-weight: 800;
    }
    
    /* ---------- ADD HERE ---------- */

[data-baseweb="popover"]{
    background:white !important;
}

[data-baseweb="menu"]{
    background:white !important;
}

[data-baseweb="menu"] *{
    color:#0f172a !important;
    font-weight:600 !important;
}

[data-baseweb="popover"] *{
    color:#0f172a !important;
}

div[role="listbox"]{
    background:white !important;
}

div[role="option"]{
    color:#0f172a !important;
    background:white !important;
}

div[role="option"]:hover{
    background:#dbeafe !important;
}

/* ---------- END ---------- */


.loader-card {
    margin-top: 18px;
    background: rgba(2, 6, 23, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
}

.orb-loader {
    width: 72px;
    height: 72px;
    margin: 0 auto 14px auto;
    border-radius: 50%;
    background: conic-gradient(from 180deg, #38bdf8, #818cf8, #f472b6, #38bdf8);
    animation: spin 1s linear infinite;
    position: relative;
}

.orb-loader::after {
    content: "";
    position: absolute;
    inset: 9px;
    border-radius: 50%;
    background: #020617;
}

.processing-title {
    font-size: 20px;
    font-weight: 900;
    color: #f8fafc !important;
}

.processing-subtitle {
    margin-top: 6px;
    color: #cbd5e1 !important;
    font-size: 14px;
}

.pipeline-dots {
    margin-top: 18px;
    display: flex;
    justify-content: center;
    gap: 10px;
}

.pipeline-dots span {
    width: 10px;
    height: 10px;
    background: #38bdf8;
    border-radius: 50%;
    animation: pulse 1.2s infinite ease-in-out;
}

.pipeline-dots span:nth-child(2) { animation-delay: 0.15s; background: #60a5fa; }
.pipeline-dots span:nth-child(3) { animation-delay: 0.30s; background: #818cf8; }
.pipeline-dots span:nth-child(4) { animation-delay: 0.45s; background: #a78bfa; }
.pipeline-dots span:nth-child(5) { animation-delay: 0.60s; background: #f472b6; }

@keyframes spin {
    to { transform: rotate(360deg); }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(0.65);
        opacity: 0.45;
    }
    50% {
        transform: scale(1.25);
        opacity: 1;
    }
}

.hero{
    margin-bottom:28px;
}

.hero-top{
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    margin-bottom:12px;
}

.language-pills{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}

.pill{
    background:rgba(56,189,248,.12);
    border:1px solid rgba(56,189,248,.35);
    padding:9px 18px;
    border-radius:999px;
    color:#e2e8f0 !important;
    font-weight:700;
}

.feature-strip{
    display:flex;
    justify-content:center;
    gap:14px;
    flex-wrap:wrap;
    margin-top:18px;
}

.feature-strip span{
    background:rgba(15,23,42,.75);
    border:1px solid rgba(148,163,184,.22);
    padding:10px 16px;
    border-radius:14px;
    font-weight:700;
    color:#e2e8f0 !important;
}

.info-card{
    background:rgba(15,23,42,.78);
    border:1px solid rgba(56,189,248,.25);
    border-radius:22px;
    padding:22px 22px 14px 22px;
    min-height:unset;
    box-shadow:0 10px 30px rgba(0,0,0,.22);
}

.info-title{

    font-size:24px;

    font-weight:900;

    margin-bottom:16px;

    color:#ffffff!important;

}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 32px;
}

.info-item{
    font-size:17px;
    color:#dbeafe!important;
    margin:10px 0;
    font-weight:600;
    display:flex;
    align-items:center;
    gap:8px;
}


[data-testid="stVerticalBlockBorderWrapper"]{
    border:none !important;
    box-shadow:none !important;
    background:transparent !important;
    border-radius:0 !important;
    padding:0 !important;
    margin:0 !important;
    min-height:0 !important;
    height:0 !important;
    overflow:hidden !important;
}

[data-testid="stForm"] {
    border:none !important;
    box-shadow:none !important;
    background:transparent !important;
    padding:0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 24px;
    padding: 26px;
    box-shadow: 0 18px 60px rgba(0,0,0,0.32);
}

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="hero">
    <div class="hero-top">
        <div class="hero-title">VoxBridge</div>
        <div class="language-pills">
            <span class="pill">🌍 English</span>
            <span class="pill">🇮🇳 Hindi</span>
            <span class="pill">🇮🇳 Marathi</span>
        </div>
    </div>
    <div class="hero-subtitle">
        Breaking language barriers — completely offline.
    </div>
    <div class="feature-strip">
        <span>🎙️ Speech Recognition</span>
        <span>🌐 Translation</span>
        <span>🔊 AI Voice</span>
        <span>📝 Subtitles</span>
        <span>🎬 Video Rendering</span>
    </div>
</div>
""",
    unsafe_allow_html=True
)

info_left, info_right = st.columns(2)

with info_left:
    st.markdown(
        """<div class="info-card">
<div class="info-title">🧠 AI Stack</div>
<div class="info-grid">
  <div class="info-item">🎙️ Faster-Whisper</div>
  <div class="info-item">🌐 NLLB-200</div>
  <div class="info-item">🔊 eSpeak-NG</div>
  <div class="info-item">🎬 FFmpeg</div>
</div>
</div>""", unsafe_allow_html=True)

with info_right:
    st.markdown(
        """<div class="info-card">
<div class="info-title">🚀 Why VoxBridge?</div>
<div class="info-grid">
  <div class="info-item">🔒 Fully Offline</div>
  <div class="info-item">⚡ Privacy First</div>
  <div class="info-item">🌍 Text • Audio • Video</div>
  <div class="info-item">📝 Speech • Voice • Subtitles</div>
</div>
</div>""", unsafe_allow_html=True)

left, right = st.columns([0.8, 1.2], gap="large")

with left:
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Configure Translation")

    with st.form("process_form"):

        uploaded_file = st.file_uploader(
            "Upload video, audio, or text",
            type=["mp4", "mov", "mkv", "avi",
                  "mp3", "wav", "m4a",
                  "aac", "flac", "txt"]
        )

        source_language = st.selectbox(
            "Source Language",
            ["auto", "en", "hi", "mr"],
            format_func=lambda x: {
                "auto": "Auto Detect",
                "en": "English",
                "hi": "Hindi",
                "mr": "Marathi"
            }[x]
        )

        target_language = st.selectbox(
            "Target Language",
            ["en", "hi", "mr"],
            format_func=lambda x: {
                "en": "English",
                "hi": "Hindi",
                "mr": "Marathi"
            }[x]
        )

        voice_gender = st.radio(
            "Voice",
            ["male", "female"],
            horizontal=True
        )

        process_clicked = st.form_submit_button(
            "Translate Now 🚀",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Processing Results")

    if not process_clicked and st.session_state.last_result is None:
        st.info("Upload a file and click Translate Now.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    if process_clicked and uploaded_file is None:
        st.error("Please upload a file first.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    if process_clicked:
        try:
            input_type = detect_input_type(uploaded_file.name)
            input_path = save_uploaded_file(uploaded_file, input_type)

            request = ProcessRequest(
                input_type=input_type,
                input_path=input_path,
                source_language=source_language,
                target_language=target_language,
                voice_gender=voice_gender
            )

            loader_placeholder = st.empty()
            progress_bar = st.progress(0)
            progress_text = st.empty()

            try:
                loader_placeholder.markdown(
                    """<div class="loader-card">
                       <div class="orb-loader"></div>
                       <div class="processing-title">VoxBridge is working its magic</div>
                       <div class="processing-subtitle">Transcribing speech · Translating text · Generating subtitles · Creating voice · Rendering video</div>
                       <div class="pipeline-dots"><span></span><span></span><span></span><span></span><span></span></div>
                       </div>""",
                    unsafe_allow_html=True
                )

                steps = [
                    (10, "📥 Upload saved"),
                    (25, "🎙️ Transcribing speech"),
                    (45, "🌍 Translating content"),
                    (65, "📝 Generating subtitles"),
                    (82, "🔊 Creating translated speech"),
                    (95, "🎬 Rendering final output"),
                ]

                for progress, label in steps:
                    progress_bar.progress(progress)
                    progress_text.markdown(f"**{label}**")
                    time.sleep(0.6)

                result = process_file(request)
                st.session_state.last_result = result
                st.session_state.last_voice_gender = voice_gender
                st.session_state.last_uploaded_file_name = uploaded_file.name

                progress_bar.progress(100)
                progress_text.markdown("**✅ Processing complete**")
                time.sleep(0.4)

            finally:
                loader_placeholder.empty()
                progress_bar.empty()
                progress_text.empty()

        except Exception as e:
            st.error(str(e))
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()

    # Always read from session_state — never re-process
    result = st.session_state.last_result
    display_voice = st.session_state.get("last_voice_gender", "-")

    st.markdown('<div class="success-box">✅ Done! VoxBridge processed your file successfully.</div>',
                unsafe_allow_html=True)

    lang_map = {"en": "English", "hi": "Hindi",
                "mr": "Marathi", "auto": "Auto"}
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f'<div class="mini-card"><div class="mini-label">Input</div><div class="mini-value">{result.get("input_type", "-")}</div></div>', unsafe_allow_html=True)
    with m2:
        detected = lang_map.get(result.get(
            "detected_language", ""), result.get("detected_language", "N/A"))
        st.markdown(
            f'<div class="mini-card"><div class="mini-label">Detected</div><div class="mini-value">{detected}</div></div>', unsafe_allow_html=True)
    with m3:
        target = lang_map.get(result.get("target_language", ""),
                              result.get("target_language", "-"))
        st.markdown(
            f'<div class="mini-card"><div class="mini-label">Target</div><div class="mini-value">{target}</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(
            f'<div class="mini-card"><div class="mini-label">Voice</div><div class="mini-value">{display_voice}</div></div>', unsafe_allow_html=True)

    translated_video = result.get("translated_video_path")
    translated_audio = result.get("translated_audio_path")

    if translated_video and os.path.exists(translated_video):
        st.markdown(
            '<div class="section-title">Final Translated Video</div>', unsafe_allow_html=True)
        st.video(translated_video)

    if translated_audio and os.path.exists(translated_audio):
        st.markdown(
            '<div class="section-title">Translated Audio</div>', unsafe_allow_html=True)
        st.audio(translated_audio)

    st.markdown('<div class="section-title">Transcript & Translation</div>',
                unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        st.text_area("Original", value=result.get("transcript_text")
                     or result.get("original_text") or "", height=190)
    with t2:
        st.text_area("Translated", value=result.get(
            "translated_text", ""), height=190)

    st.markdown('<div class="section-title">Download Outputs</div>',
                unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("##### 🎬 Media")
        download_button("🎥 Final Video", result.get(
            "translated_video_path"), "video/mp4")
        download_button("🔊 Translated Audio", result.get(
            "translated_audio_path"), "audio/wav")
    with d2:
        st.markdown("##### 📄 Text")
        download_button("📄 Transcript", result.get(
            "transcript_path"), "text/plain")
        download_button("🌍 Translation", result.get(
            "translated_text_path"), "text/plain")
    with d3:
        st.markdown("##### 💬 Subtitles")
        download_button("📝 Original SRT", result.get(
            "original_subtitle_path"), "text/plain")
        download_button("📝 Translated SRT", result.get(
            "translated_subtitle_path"), "text/plain")

    with st.expander("Debug JSON"):
        st.json(result)

    st.markdown("</div>", unsafe_allow_html=True)
