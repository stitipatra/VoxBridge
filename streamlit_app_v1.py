import os
import time
import base64
from pathlib import Path

import streamlit as st

from app.routes.process import ProcessRequest, process_file


st.set_page_config(
    page_title="अनुवादिनी | Breaking Language Barriers",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Session State
# -----------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_uploaded_file_name" not in st.session_state:
    st.session_state.last_uploaded_file_name = None

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Home"


# -----------------------------
# Helpers
# -----------------------------
def image_to_base64(path: str) -> str:
    image_path = Path(path)
    if not image_path.exists():
        return ""
    return base64.b64encode(image_path.read_bytes()).decode()


def detect_input_type(filename: str) -> str:
    extension = os.path.splitext(filename)[1].lower()
    video_extensions = {".mp4", ".mov", ".mkv", ".avi"}
    audio_extensions = {".mp3", ".wav", ".m4a", ".aac", ".flac"}
    text_extensions = {".txt", ".srt", ".docx", ".pdf"}

    if extension in video_extensions:
        return "video"
    if extension in audio_extensions:
        return "audio"
    if extension in text_extensions:
        return "text"
    raise ValueError(f"Unsupported file type: {extension}")


def save_uploaded_file(uploaded_file, input_type: str) -> str:
    upload_dir = os.path.join("storage", "uploads", input_type)
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = os.path.basename(uploaded_file.name)
    file_path = os.path.join(upload_dir, safe_name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path


def download_button(label: str, file_path: str | None, mime: str):
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as file:
            st.download_button(
                label=label,
                data=file,
                file_name=os.path.basename(file_path),
                mime=mime,
                use_container_width=True,
            )
    else:
        st.button(label, disabled=True, use_container_width=True)


def get_video_display_layout(video_path: str) -> tuple[list[float], int]:
    """Return centered Streamlit column ratios and a max height for video preview.
    The preview is intentionally compact so a video never takes over the page.
    No backend changes are needed; this only controls the frontend preview size.
    """
    try:
        import cv2  # optional, only used for local preview sizing
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        cap.release()

        if width > 0 and height > 0:
            # Portrait/reel videos should look like reels, not giant page-wide videos.
            if height > width:
                return [1.85, 0.9, 1.85], 430

            # Landscape videos still stay centered and demo-friendly.
            if width / max(height, 1) >= 1.55:
                return [0.95, 1.45, 0.95], 360

            # Square-ish videos.
            return [1.25, 1.25, 1.25], 390
    except Exception:
        pass

    return [1.05, 1.35, 1.05], 380


def language_label(code: str | None) -> str:
    return {
        "auto": "Auto Detect",
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
    }.get(code or "", code or "N/A")


def metric_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mode_config(mode: str):
    configs = {
        "Text Translation": {
            "title": "Text Translation",
            "subtitle": "Upload .txt or .srt files and translate them locally.",
            "types": ["txt", "srt", "docx", "pdf"],
            "icon": "⌁",
        },
        "Audio Translation": {
            "title": "Audio Translation",
            "subtitle": "Upload audio, transcribe speech, translate it, and export translated audio.",
            "types": ["mp3", "wav", "m4a", "aac", "flac"],
            "icon": "◉",
        },
        "Video Translation": {
            "title": "Video Translation",
            "subtitle": "Upload video, translate spoken content, and generate subtitle-ready output.",
            "types": ["mp4", "mov", "mkv", "avi"],
            "icon": "▶",
        },
    }
    return configs.get(
        mode,
        {
            "title": "Upload your file",
            "subtitle": "Choose text, audio or video — Anuwadini keeps the backend pipeline unchanged.",
            "types": ["mp4", "mov", "mkv", "avi", "mp3", "wav", "m4a", "aac", "flac", "txt", "srt", "docx", "pdf"],
            "icon": "＋",
        },
    )


hsbc_logo = image_to_base64("assets/hsbc_logo.png")
baif_logo = image_to_base64("assets/baif.png")
hsbc_img = f'<img src="data:image/png;base64,{hsbc_logo}" alt="HSBC" />' if hsbc_logo else '<div class="logo-fallback">HSBC</div>'
baif_img = f'<img src="data:image/png;base64,{baif_logo}" alt="BAIF" />' if baif_logo else '<div class="logo-fallback">BAIF</div>'


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=Noto+Sans+Devanagari:wght@600;700;800;900&display=swap');

        :root {
            --blue-950: #062f6f;
            --blue-900: #083f8f;
            --blue-800: #0b4ea2;
            --blue-700: #1164c7;
            --blue-100: #eaf4ff;
            --blue-050: #f5faff;
            --ink: #0d1b2f;
            --muted: #53657d;
            --line: #d7e7fb;
            --card: rgba(255, 255, 255, 0.92);
            --shadow: 0 20px 50px rgba(11, 58, 127, 0.12);
            --font: "Inter", "Noto Sans Devanagari", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        html { scroll-behavior: smooth; }
        header[data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }

        .stApp {
            font-family: var(--font);
            color: var(--ink);
            background:
                radial-gradient(circle at 78% -8%, rgba(151, 200, 255, .38), transparent 25%),
                radial-gradient(circle at 5% 8%, rgba(62, 137, 226, .20), transparent 25%),
                linear-gradient(180deg, #f6fbff 0%, #eef6ff 44%, #f8fbff 100%);
        }

        .block-container {
            max-width: 1500px;
            padding-top: .55rem;
            padding-left: .9rem;
            padding-right: .9rem;
            padding-bottom: 1.2rem;
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 50% 0%, rgba(117, 180, 255, .24), transparent 30%),
                linear-gradient(180deg, #0d5db4 0%, #094995 48%, #062f6f 100%);
            border-right: 1px solid rgba(255,255,255,.16);
        }
        section[data-testid="stSidebar"] > div { padding-top: 1rem; }
        section[data-testid="stSidebar"] .stButton { margin-bottom: 10px; }
        section[data-testid="stSidebar"] .stButton button {
            height: 54px !important;
            border-radius: 18px !important;
            background: rgba(255,255,255,.09) !important;
            border: 1px solid rgba(255,255,255,.12) !important;
            color: white !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 12px 24px rgba(0,0,0,.08) !important;
            font-weight: 850 !important;
            letter-spacing: -.15px !important;
            transition: all .18s ease !important;
            justify-content: flex-start !important;
            padding-left: 22px !important;
        }
        section[data-testid="stSidebar"] .stButton button p {
            font-size: 15.5px !important;
            text-align: left !important;
            width: 100%;
        }
        section[data-testid="stSidebar"] .stButton button:hover {
            background: rgba(255,255,255,.18) !important;
            border-color: rgba(255,255,255,.26) !important;
            transform: translateX(4px);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.16), 0 18px 34px rgba(0,0,0,.14) !important;
        }

        .sidebar-about {
            margin-top: 28px;
            border: 1px solid rgba(255,255,255,.20);
            border-radius: 22px;
            padding: 22px 16px;
            color: white;
            text-align: center;
            background: rgba(255,255,255,.07);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.14);
        }
        .sidebar-about-title { font-size: 26px; font-weight: 950; margin-bottom: 6px; }
        .sidebar-about-sub { font-size: 14px; font-weight: 850; margin-bottom: 12px; }
        .sidebar-about-text { font-size: 13px; line-height: 1.65; opacity: .92; }
        .sidebar-version { margin-top: 14px; font-size: 13px; opacity: .90; }

        .top-brand-header {
            min-height: 160px;
            position: relative;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(255,255,255,.98), rgba(247,251,255,.95));
            border: 1px solid rgba(164, 205, 252, .9);
            box-shadow: var(--shadow);
            overflow: visible;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 18px;
        }
        .top-brand-header::before {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 50% -18%, rgba(17,100,199,.12), transparent 38%);
            pointer-events: none;
        }
        .brand-logo-left, .brand-logo-right {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            z-index: 2;
        }
        .brand-logo-left { left: 58px; }
        .brand-logo-right { right: 58px; }
        .brand-logo-left img { max-height: 74px; max-width: 190px; object-fit: contain; }
        .brand-logo-right img { max-height: 76px; max-width: 180px; object-fit: contain; }
        .logo-fallback { color: var(--blue-900); font-weight: 950; font-size: 28px; }
        .brand-center { text-align: center; z-index: 2; padding: 14px 210px 12px 210px; }
        .brand-title {
            font-family: "Noto Sans Devanagari", var(--font);
            font-size: clamp(42px, 4vw, 60px);
            line-height: 1.05;
            font-weight: 950;
            letter-spacing: -2px;
            color: var(--blue-900);
        }
        .brand-subtitle {
            margin-top: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            color: var(--blue-900);
            font-size: clamp(16px, 1.45vw, 22px);
            font-weight: 700;
            font-style: italic;
        }
        .brand-subtitle::before, .brand-subtitle::after {
            content: "";
            width: 92px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--blue-700));
        }
        .brand-subtitle::after { background: linear-gradient(90deg, var(--blue-700), transparent); }
        .brand-dot { width: 7px; height: 7px; border-radius: 999px; background: var(--blue-900); display: inline-block; }

        .page-shell {
            border-radius: 28px;
            background: rgba(255,255,255,.58);
            border: 1px solid rgba(188, 218, 253, .78);
            box-shadow: var(--shadow);
            padding: 24px;
            backdrop-filter: blur(16px);
        }

        .welcome-card {
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 24px 30px;
            min-height: 132px;
            background:
                radial-gradient(circle at 86% 45%, rgba(17,100,199,.12), transparent 25%),
                linear-gradient(135deg, rgba(255,255,255,.96), rgba(247,251,255,.94));
            display: grid;
            grid-template-columns: 74px 1fr 360px;
            gap: 22px;
            align-items: center;
            box-shadow: 0 12px 30px rgba(11, 58, 127, .08);
        }
        .welcome-icon {
            width: 64px;
            height: 64px;
            display: grid;
            place-items: center;
            border-radius: 22px;
            color: white;
            font-size: 30px;
            background: linear-gradient(135deg, var(--blue-700), var(--blue-950));
            box-shadow: 0 16px 30px rgba(11, 78, 162, .22);
        }
        .welcome-title { color: var(--blue-950); font-size: 25px; font-weight: 950; margin-bottom: 8px; letter-spacing: -.4px; }
        .welcome-text { color: #233553; font-size: 15.5px; line-height: 1.55; font-weight: 600; }
        .world-map {
            height: 78px;
            opacity: .34;
            background-image: radial-gradient(var(--blue-700) 1.45px, transparent 1.45px);
            background-size: 8px 8px;
            clip-path: polygon(2% 35%, 16% 19%, 30% 33%, 45% 17%, 56% 38%, 74% 20%, 98% 37%, 88% 80%, 70% 62%, 56% 84%, 42% 61%, 26% 78%, 11% 61%);
        }

        .feature-grid {
            margin-top: 20px;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 20px;
        }
        .feature-card {
            border-radius: 24px;
            border: 1px solid rgba(186, 216, 251, .9);
            background: linear-gradient(135deg, rgba(255,255,255,.98), rgba(247,251,255,.95));
            padding: 22px;
            min-height: 150px;
            display: grid;
            grid-template-columns: 66px 1fr;
            gap: 18px;
            align-items: center;
            box-shadow: 0 18px 42px rgba(11, 58, 127, .10);
            transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            border-color: rgba(17,100,199,.45);
            box-shadow: 0 24px 56px rgba(11, 58, 127, .16);
        }
        .feature-icon {
            width: 66px;
            height: 66px;
            border-radius: 22px;
            display: grid;
            place-items: center;
            color: var(--blue-900);
            background: linear-gradient(135deg, #eef7ff, #cfe6ff);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.9);
            font-size: 30px;
            font-weight: 950;
        }
        .feature-title { color: var(--blue-950); font-size: 21px; font-weight: 950; letter-spacing: -.35px; margin-bottom: 8px; }
        .feature-text { color: #35445b; font-size: 14.5px; line-height: 1.48; font-weight: 600; margin-bottom: 10px; }
        .feature-link {
            color: var(--blue-800) !important;
            text-decoration: none !important;
            font-weight: 900;
            font-size: 14px;
        }
        .feature-link:hover { text-decoration: underline !important; text-underline-offset: 4px; }

        .upload-anchor { scroll-margin-top: 16px; }
        .upload-panel, .result-panel, .configure-panel, .info-card, .history-card {
            margin-top: 22px;
            border-radius: 26px;
            background: linear-gradient(135deg, rgba(255,255,255,.98), rgba(248,252,255,.96));
            border: 1px solid var(--line);
            box-shadow: 0 18px 42px rgba(11, 58, 127, .10);
            padding: 24px;
            color: var(--ink);
        }
        .upload-head { display: flex; align-items: center; gap: 14px; justify-content: center; margin-bottom: 16px; }
        .upload-badge {
            width: 44px; height: 44px; border-radius: 16px; display: grid; place-items: center;
            background: linear-gradient(135deg, var(--blue-700), var(--blue-950)); color: white; font-size: 22px; font-weight: 950;
        }
        .upload-title { color: var(--blue-950); font-size: 24px; font-weight: 950; letter-spacing: -.4px; }
        .upload-subtitle { color: var(--muted); font-size: 14.5px; font-weight: 650; margin-top: 2px; }

        div[data-testid="stForm"] {
            background: transparent;
            border: 0;
            padding: 0;
        }
        div[data-testid="stFileUploader"] section {
            background: #ffffff !important;
            border: 1.5px dashed #8bbdf5 !important;
            border-radius: 18px !important;
            min-height: 84px !important;
        }
        div[data-testid="stFileUploader"] * { color: #182941 !important; }
        div[data-testid="stFileUploader"] small, div[data-testid="stFileUploader"] p { color: #6b7890 !important; }
        .stSelectbox label, .stRadio label, .stFileUploader label, .stTextArea label {
            color: #13243d !important;
            font-weight: 850 !important;
        }
        div[data-baseweb="select"] > div {
            border-radius: 15px !important;
            border: 1px solid var(--line) !important;
            background: #ffffff !important;
            min-height: 48px !important;
        }
        div[data-baseweb="select"] * { color: var(--ink) !important; }
        div[role="radiogroup"] * { color: #25344d !important; }

        .stButton button, .stFormSubmitButton button {
            border-radius: 16px !important;
            min-height: 48px !important;
            background: linear-gradient(135deg, #1164c7, #083f8f) !important;
            color: #ffffff !important;
            border: 0 !important;
            font-weight: 900 !important;
            box-shadow: 0 16px 30px rgba(11, 78, 162, .22) !important;
            transition: all .18s ease !important;
        }
        .stButton button:hover, .stFormSubmitButton button:hover {
            transform: translateY(-1px);
            background: linear-gradient(135deg, #0e59b4, #062f6f) !important;
        }
        .stDownloadButton button {
            background: #ffffff !important;
            color: var(--blue-900) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
            height: 45px !important;
            font-weight: 850 !important;
            box-shadow: none !important;
        }
        .stDownloadButton button:hover { background: var(--blue-100) !important; }

        .section-title {
            color: var(--blue-950);
            font-size: 24px;
            font-weight: 950;
            letter-spacing: -.4px;
            margin: 8px 0 16px 0;
        }
        .mini-muted, .configure-panel p, .configure-panel li, .history-card p, .info-card p {
            color: #43546c !important;
            font-size: 15px;
            line-height: 1.65;
            font-weight: 600;
        }
        .configure-panel h1, .configure-panel h2, .configure-panel h3, .configure-panel h4,
        .history-card h1, .history-card h2, .history-card h3,
        .info-card h1, .info-card h2, .info-card h3 {
            color: var(--blue-950) !important;
        }
        code {
            color: #0b5db8 !important;
            background: #edf6ff !important;
            border: 1px solid #d3e8ff;
            padding: 2px 7px !important;
            border-radius: 8px !important;
        }

        .success-box {
            color: #075c36;
            background: linear-gradient(135deg, #eafff3, #f7fffb);
            border: 1px solid #bcebd1;
            box-shadow: none;
            padding: 14px 16px;
            border-radius: 18px;
            font-weight: 900;
            margin-bottom: 18px;
        }
        .metric-card {
            min-height: 90px;
            border-radius: 20px;
            background: linear-gradient(135deg, #ffffff, #f3f8ff);
            border: 1px solid var(--line);
            padding: 16px;
            box-shadow: 0 10px 24px rgba(11, 58, 127, .08);
        }
        .metric-label { color: #64748b; font-size: 11px; font-weight: 950; text-transform: uppercase; letter-spacing: .9px; margin-bottom: 9px; }
        .metric-value { color: var(--blue-950); font-size: 21px; font-weight: 950; text-transform: capitalize; word-break: break-word; }

        .video-shell {
            margin: 0 auto 18px auto;
            border-radius: 26px;
            padding: 10px;
            background: linear-gradient(135deg, #ffffff, #edf6ff);
            border: 1px solid var(--line);
            box-shadow: 0 18px 42px rgba(11, 58, 127, .12);
            max-width: 680px;
        }
        .video-shell [data-testid="stVideo"] { width: 100% !important; }
        .video-shell video {
            width: 100% !important;
            object-fit: contain !important;
            border-radius: 20px !important;
            background: #000 !important;
        }

        .stTextArea textarea {
            color: var(--ink) !important;
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            border-radius: 16px !important;
        }
        .streamlit-expanderHeader, details summary, details * { color: var(--ink) !important; }
        div[data-testid="stJson"] * { color: var(--ink) !important; }

        .format-row { display:flex; flex-wrap:wrap; gap:8px; margin: 12px 0 24px 0; }
        .pill { background:#edf6ff; color:#0b4ea2; border:1px solid #d2e8ff; padding:6px 10px; border-radius:999px; font-weight:850; font-size:13px; }
        .footer-note { text-align:center; color:#38506d; font-size:14px; font-weight:750; padding:18px 0 4px 0; }



        .loader-card {
            border-radius: 26px;
            padding: 28px 24px;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #f1f8ff 100%);
            border: 1px solid #cfe4fb;
            box-shadow: 0 18px 46px rgba(11, 58, 127, .12);
            margin: 12px 0 14px 0;
        }
        .orb-loader {
            width: 70px; height: 70px; border-radius: 50%;
            margin: 0 auto 16px auto;
            background: conic-gradient(from 180deg, #0b4ea2, #25a7df, #7c7ff2, #e47bd2, #0b4ea2);
            animation: spin 1s linear infinite;
            position: relative;
        }
        .orb-loader::after {
            content: ""; position: absolute; inset: 11px;
            border-radius: 50%; background: #ffffff;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .processing-title {
            color: var(--blue-950); font-size: 22px; font-weight: 950; margin-bottom: 8px;
        }
        .processing-subtitle {
            color: #42536b; font-size: 14.5px; font-weight: 700; line-height: 1.5;
        }
        .pipeline-dots {
            display: flex; justify-content: center; gap: 10px; margin-top: 18px;
        }
        .pipeline-dots span {
            width: 11px; height: 11px; border-radius: 999px;
            background: #25a7df; animation: pulse 1.15s infinite ease-in-out;
        }
        .pipeline-dots span:nth-child(2) { background: #62b6ff; animation-delay: .12s; }
        .pipeline-dots span:nth-child(3) { background: #7c7ff2; animation-delay: .24s; }
        .pipeline-dots span:nth-child(4) { background: #9a79df; animation-delay: .36s; }
        .pipeline-dots span:nth-child(5) { background: #e47bd2; animation-delay: .48s; }
        @keyframes pulse {
            0%, 100% { transform: scale(.78); opacity: .45; }
            50% { transform: scale(1.22); opacity: 1; }
        }
        .progress-percent {
            color: var(--blue-900); font-weight: 950; margin-top: 10px; font-size: 14px;
        }

        @media (max-width: 1050px) {
            .brand-logo-left, .brand-logo-right { position: static; transform: none; justify-content:center; }
            .top-brand-header { display:grid; grid-template-columns: 1fr; gap:10px; padding:18px; }
            .brand-center { padding:0; }
            .welcome-card { grid-template-columns: 1fr; text-align:center; }
            .welcome-icon { margin:auto; }
            .world-map { display:none; }
            .feature-grid { grid-template-columns: 1fr; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"""
    <div class="top-brand-header">
        <div class="brand-logo-left">{hsbc_img}</div>
        <div class="brand-center">
            <div class="brand-title">अनुवादिनी</div>
            <div class="brand-subtitle"><span class="brand-dot"></span>Breaking Language Barriers<span class="brand-dot"></span></div>
        </div>
        <div class="brand-logo-right">{baif_img}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    nav_options = [
        ("Home", "⌂"),
        ("Text Translation", "A↔अ"),
        ("Audio Translation", "◉"),
        ("Video Translation", "▶"),
        ("History", "↺"),
        ("Settings", "⚙"),
        ("About", "ⓘ"),
    ]
    for label, icon in nav_options:
        prefix = "● " if st.session_state.selected_mode == label else ""
        if st.button(f"{prefix}{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.selected_mode = label
            st.rerun()

    st.markdown(
        """
        <div class="sidebar-about">
            <div class="sidebar-about-title">अनुवादिनी</div>
            <div class="sidebar-about-sub">Breaking Language Barriers</div>
            <div class="sidebar-about-text">
                Offline AI-powered translation<br>
                for text, audio and video.
            </div>
            <div class="sidebar-version">v1.0.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="page-shell">', unsafe_allow_html=True)


# -----------------------------
# Translation Pages
# -----------------------------
if st.session_state.selected_mode in ["Home", "Text Translation", "Audio Translation", "Video Translation"]:
    selected_mode = st.session_state.selected_mode
    cfg = mode_config(selected_mode)

    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">☰</div>
            <div>
                <div class="welcome-title">Welcome to अनुवादिनी</div>
                <div class="welcome-text">
                    A privacy-first offline platform for translating text, audio and video across Indian languages.
                    Built for accessibility and field. 
                </div>
            </div>
            <div class="world-map"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">अ</div>
                <div>
                    <div class="feature-title">Text Translation</div>
                    <div class="feature-text">Translate documents, subtitles and typed content with clean local-language output.</div>
                    <a class="feature-link" href="#upload-section">Use text workflow →</a>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎙</div>
                <div>
                    <div class="feature-title">Audio Translation</div>
                    <div class="feature-text">Transcribe speech, translate it offline and export translated audio assets.</div>
                    <a class="feature-link" href="#upload-section">Use audio workflow →</a>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">▶</div>
                <div>
                    <div class="feature-title">Video Translation</div>
                    <div class="feature-text">Translate spoken video content and generate subtitle-ready multilingual output.</div>
                    <a class="feature-link" href="#upload-section">Use video workflow →</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div id="upload-section" class="upload-anchor"></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="upload-head">
            <div class="upload-badge">{cfg['icon']}</div>
            <div>
                <div class="upload-title">{cfg['title']}</div>
                <div class="upload-subtitle">{cfg['subtitle']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("process_form"):
        uploaded_file = st.file_uploader("Browse Files", type=cfg["types"])

        c1, c2, c3 = st.columns([1, 1, 0.85], gap="large")
        with c1:
            source_language = st.selectbox(
                "Source Language",
                ["auto", "en", "hi", "mr"],
                format_func=language_label,
            )
        with c2:
            target_language = st.selectbox(
                "Target Language",
                ["en", "hi", "mr"],
                format_func=language_label,
                index=1,
            )
        with c3:
            voice_gender = st.radio(
                "Voice", ["male", "female"], horizontal=True)

        process_clicked = st.form_submit_button(
            "Translate Now  →", use_container_width=True)

    st.caption("Supported formats in this view: " +
               ", ".join([f".{x}" for x in cfg["types"]]))
    st.markdown('</div>', unsafe_allow_html=True)

    if process_clicked and uploaded_file is None:
        st.error("Please upload a file first.")

    if process_clicked and uploaded_file is not None:
        try:
            input_type = detect_input_type(uploaded_file.name)
            input_path = save_uploaded_file(uploaded_file, input_type)

            request = ProcessRequest(
                input_type=input_type,
                input_path=input_path,
                source_language=source_language,
                target_language=target_language,
                voice_gender=voice_gender,
            )

            loader_placeholder = st.empty()
            progress_bar = st.progress(0)
            progress_text = st.empty()

            try:
                loader_placeholder.markdown(
                    """
                    <div class="loader-card">
                        <div class="orb-loader"></div>
                        <div class="processing-title">अनुवादिनी is working its magic</div>
                        <div class="processing-subtitle">Transcribing speech · Translating text · Generating subtitles · Creating voice · Rendering video</div>
                        <div class="pipeline-dots"><span></span><span></span><span></span><span></span><span></span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for progress, label in [
                    (10, "📥 Upload saved"),
                    (25, "🎙️ Transcribing speech"),
                    (45, "🌐 Translating content"),
                    (65, "📝 Generating subtitles"),
                    (82, "🔊 Creating translated speech"),
                    (95, "🎬 Rendering final output"),
                ]:
                    progress_bar.progress(progress)
                    progress_text.markdown(
                        f"**{label}** &nbsp; <span class='progress-percent'>{progress}%</span>", unsafe_allow_html=True)
                    time.sleep(0.25)

                result = process_file(request)
                st.session_state.last_result = result
                st.session_state.last_uploaded_file_name = uploaded_file.name
                progress_bar.progress(100)
                progress_text.markdown(
                    "**✅ Processing complete** &nbsp; <span class='progress-percent'>100%</span>", unsafe_allow_html=True)
                time.sleep(0.35)
            finally:
                loader_placeholder.empty()
                progress_bar.empty()
                progress_text.empty()
        except Exception as e:
            st.error(str(e))

    if st.session_state.last_result is not None:
        result = st.session_state.last_result
        st.markdown('<div class="result-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="success-box">✅ Done! Anuwadini processed your file successfully.</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card("Input", result.get("input_type", "-"))
        with m2:
            metric_card("Detected", language_label(
                result.get("detected_language", "N/A")))
        with m3:
            metric_card("Target", language_label(
                result.get("target_language", "-")))
        with m4:
            metric_card(
                "File", st.session_state.last_uploaded_file_name or "-")

        translated_video = result.get("translated_video_path")
        translated_audio = result.get("translated_audio_path")

        if translated_video and os.path.exists(translated_video):
            st.markdown(
                '<div class="section-title">Final Translated Video</div>', unsafe_allow_html=True)
            video_cols, video_max_height = get_video_display_layout(
                translated_video)
            left_spacer, video_col, right_spacer = st.columns(video_cols)
            with video_col:
                st.markdown('<div class="video-shell">',
                            unsafe_allow_html=True)
                st.video(translated_video)
                st.markdown(
                    f"<style>.video-shell video {{ max-height: {video_max_height}px !important; }}</style>",
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

        if translated_audio and os.path.exists(translated_audio):
            st.markdown(
                '<div class="section-title">Translated Audio</div>', unsafe_allow_html=True)
            st.audio(translated_audio)

        st.markdown(
            '<div class="section-title">Transcript & Translation</div>', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            st.text_area("Original", value=result.get("transcript_text")
                         or result.get("original_text") or "", height=180)
        with t2:
            st.text_area("Translated", value=result.get(
                "translated_text", ""), height=180)

        st.markdown(
            '<div class="section-title">Download Outputs</div>', unsafe_allow_html=True)
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
            download_button("🌐 Translation", result.get(
                "translated_text_path"), "text/plain")
        with d3:
            st.markdown("##### 💬 Subtitles")
            download_button("📝 Original SRT", result.get(
                "original_subtitle_path"), "text/plain")
            download_button("📝 Translated Subtitles", result.get(
                "translated_subtitle_path"), "text/plain")

        with st.expander("Debug JSON"):
            st.json(result)
        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# History Page
# -----------------------------
elif st.session_state.selected_mode == "History":
    st.markdown('<div class="history-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">↺ Translation History</div>',
                unsafe_allow_html=True)
    if st.session_state.last_result:
        st.success(
            f"Last processed file: {st.session_state.last_uploaded_file_name}")
        with st.expander("Last result JSON", expanded=True):
            st.json(st.session_state.last_result)
    else:
        st.info("No translation has been processed in this session yet.")
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Settings Page
# -----------------------------
elif st.session_state.selected_mode == "Settings":
    st.markdown('<div class="configure-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙ Settings</div>',
                unsafe_allow_html=True)
    st.markdown(
        """
        <div class="mini-muted">
            Current hackathon build keeps the backend unchanged and uses the same local processing pipeline.
            Add new model paths, language pairs, upload limits, or deployment settings in the backend config.
        </div>
        <h3>Supported Input Types</h3>
        <div class="format-row">
            <span class="pill">.txt</span><span class="pill">.srt</span><span class="pill">.docx</span><span class="pill">.pdf</span><span class="pill">.mp3</span><span class="pill">.wav</span>
            <span class="pill">.m4a</span><span class="pill">.aac</span><span class="pill">.flac</span><span class="pill">.mp4</span>
            <span class="pill">.mov</span><span class="pill">.mkv</span><span class="pill">.avi</span>
        </div>
        <h3>Supported Languages</h3>
        <div class="mini-muted">English, Hindi and Marathi in this build.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# About Page
# -----------------------------
elif st.session_state.selected_mode == "About":
    a1, a2 = st.columns([1, 1], gap="large")
    with a1:
        st.markdown(
            """
            <div class="info-card">
                <div class="section-title">🧠 AI Stack</div>
                <div class="mini-muted">
                    🎙️ Faster-Whisper for speech recognition<br>
                    🌐 NLLB-200 for neural translation<br>
                    🔊 eSpeak NG for offline voice synthesis<br>
                    📝 Subtitle generation for translated output<br>
                    🎬 FFmpeg for media extraction and rendering<br>
                    ⚡ Streamlit frontend with existing backend services
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with a2:
        st.markdown(
            """
            <div class="info-card">
                <div class="section-title">🚀 Hackathon Highlights</div>
                <div class="mini-muted">
                    ✅ Offline-first and privacy-friendly<br>
                    ✅ Text, audio and video translation in one place<br>
                    ✅ Built for accessibility and language inclusion<br>
                    ✅ HSBC + BAIF branded hackathon interface<br>
                    ✅ Downloadable media, text and subtitle outputs<br>
                    ✅ Clean demo-ready single page workflow
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer-note">
        © 2026 अनुवादिनी &nbsp; | &nbsp; Breaking Language Barriers &nbsp; | &nbsp; Offline • Private • Secure
    </div>
    """,
    unsafe_allow_html=True,
)
