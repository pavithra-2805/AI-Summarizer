import streamlit as st
from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import time
import re
import requests
from urllib.parse import urlparse

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp { background: #0a0a0f; color: #e8e6f0; }

section[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #2a2a3d;
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.hero-header { text-align: center; padding: 2rem 0 1rem; }
.hero-title {
    font-size: 3.8rem; font-weight: 800; letter-spacing: -2px;
    background: linear-gradient(135deg, #c8b6ff 0%, #7c6fff 50%, #4ecaff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1; margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-family: 'DM Mono', monospace; font-size: 0.85rem;
    color: #6b6b8a; letter-spacing: 3px; text-transform: uppercase;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c6fff22, #4ecaff22);
    border: 1px solid #7c6fff55; border-radius: 20px;
    padding: 4px 16px; font-size: 0.75rem;
    font-family: 'DM Mono', monospace; color: #7c6fff;
    letter-spacing: 2px; margin-bottom: 1.2rem;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3d, transparent);
    margin: 1.2rem 0;
}

/* Tabs override */
.stTabs [data-baseweb="tab-list"] {
    background: #12121f;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #2a2a3d;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #6b6b8a;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    padding: 8px 20px;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c6fff, #4ecaff) !important;
    color: #0a0a0f !important;
    font-weight: 700;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"]    { display: none; }

/* Inputs */
textarea {
    background: #12121f !important; border: 1px solid #2a2a3d !important;
    border-radius: 12px !important; color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.88rem !important;
    padding: 1rem !important;
}
textarea:focus {
    border-color: #7c6fff !important;
    box-shadow: 0 0 0 3px #7c6fff22 !important;
}

input[type="text"] {
    background: #12121f !important; border: 1px solid #2a2a3d !important;
    border-radius: 10px !important; color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.88rem !important;
}
input[type="text"]:focus { border-color: #7c6fff !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: #12121f;
    border: 2px dashed #2a2a3d;
    border-radius: 14px;
    padding: 1.5rem;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover { border-color: #7c6fff55; }
[data-testid="stFileUploader"] label { color: #6b6b8a !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c6fff, #4ecaff) !important;
    color: #0a0a0f !important; border: none !important;
    border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    letter-spacing: 1px !important; padding: 0.7rem 2rem !important;
    width: 100% !important; transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px #7c6fff44 !important;
}

/* Source badge */
.source-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #7c6fff11; border: 1px solid #7c6fff44;
    border-radius: 8px; padding: 4px 12px;
    font-family: 'DM Mono', monospace; font-size: 0.72rem;
    color: #7c6fff; margin-bottom: 0.6rem;
}

/* Extracted preview */
.extracted-box {
    background: #0d0d18; border: 1px solid #2a2a3d;
    border-radius: 12px; padding: 1.25rem;
    font-family: 'DM Mono', monospace; font-size: 0.78rem;
    color: #6b6b8a; line-height: 1.7; max-height: 180px;
    overflow-y: auto; margin-bottom: 1rem;
    white-space: pre-wrap;
}

/* Summary output */
.summary-box {
    background: linear-gradient(135deg, #12121f, #0f0f1a);
    border: 1px solid #7c6fff44; border-radius: 16px;
    padding: 2rem; margin-top: 0;
    position: relative; overflow: hidden; min-height: 320px;
}
.summary-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: linear-gradient(90deg, #7c6fff, #4ecaff, #7c6fff);
}
.summary-label {
    font-family: 'DM Mono', monospace; font-size: 0.7rem;
    letter-spacing: 3px; color: #7c6fff;
    text-transform: uppercase; margin-bottom: 1rem;
}
.summary-text { font-size: 1rem; line-height: 1.85; color: #d8d6e8; }

.empty-box {
    background: #12121f; border: 1px dashed #2a2a3d; border-radius: 16px;
    min-height: 320px; display: flex; align-items: center;
    justify-content: center; flex-direction: column; gap: 0.75rem;
}

/* Stats */
.stat-row { display: flex; gap: 1rem; margin-top: 1.5rem; }
.stat-card {
    flex: 1; background: #12121f; border: 1px solid #2a2a3d;
    border-radius: 10px; padding: 1rem; text-align: center;
}
.stat-number {
    font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, #c8b6ff, #4ecaff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    color: #6b6b8a; letter-spacing: 2px; text-transform: uppercase; margin-top: 4px;
}

/* Sidebar */
.sidebar-title {
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    letter-spacing: 3px; color: #7c6fff;
    text-transform: uppercase; margin-bottom: 0.75rem;
}
.tech-tag {
    display: inline-block; background: #1a1a2e; border: 1px solid #2a2a3d;
    border-radius: 6px; padding: 2px 10px;
    font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #6b6b8a; margin: 2px;
}
.tech-tag.active { border-color: #7c6fff55; color: #7c6fff; background: #7c6fff11; }

.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c6fff, #4ecaff) !important;
}
.stAlert { background: #12121f !important; border-color: #7c6fff44 !important; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────
def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

def count_sentences(text):
    return max(1, len([s for s in re.split(r'[.!?]+', text.strip()) if s.strip()]))

def is_youtube_url(url):
    return any(x in url for x in ["youtube.com/watch", "youtu.be/", "youtube.com/shorts"])

def get_youtube_id(url):
    patterns = [
        r'v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'shorts/([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


# ─── Text Extraction: YouTube Transcript ──────────────────────────────────────
def extract_youtube_transcript(url: str) -> str:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        raise ImportError("Run: pip install youtube-transcript-api")

    vid_id = get_youtube_id(url)
    if not vid_id:
        raise ValueError("Could not parse YouTube video ID from URL.")

    try:
        # New API (>= 1.0.0): must instantiate first, then call fetch()
        ytt_api = YouTubeTranscriptApi()
        transcript_obj = ytt_api.fetch(vid_id)
        text = " ".join([t.text for t in transcript_obj])
    except AttributeError:
        # Fallback for older API (< 1.0.0): get_transcript() is a classmethod
        transcript_list = YouTubeTranscriptApi.get_transcript(vid_id)
        text = " ".join([t["text"] for t in transcript_list])
    return re.sub(r"\s+", " ", text).strip()

# ─── Text Extraction: Web URL ─────────────────────────────────────────────────
def extract_text_from_url(url: str) -> str:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ImportError("Run: pip install beautifulsoup4")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script","style","nav","footer","header","aside","form","noscript","iframe"]):
        tag.decompose()

    for sel in ["article","main",'[role="main"]',".post-content",
                ".article-body",".entry-content",".content","body"]:
        block = soup.select_one(sel)
        if block:
            t = block.get_text(separator=" ", strip=True)
            if len(t.split()) > 80:
                return re.sub(r'\s+', ' ', t).strip()

    return re.sub(r'\s+', ' ', soup.get_text(separator=" ", strip=True)).strip()


# ─── Text Extraction: Uploaded File ──────────────────────────────────────────
def extract_text_from_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()

    if name.endswith(".txt") or name.endswith(".md"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    elif name.endswith(".pdf"):
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("Run: pip install pdfplumber")
        parts = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
        return "\n".join(parts)

    elif name.endswith(".docx"):
        try:
            import docx
        except ImportError:
            raise ImportError("Run: pip install python-docx")
        doc = docx.Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    elif name.endswith(".csv"):
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        return " ".join(content.splitlines()[:150])

    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}")


# ─── BART Model ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(model_name="facebook/bart-large-cnn"):
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model     = BartForConditionalGeneration.from_pretrained(model_name)
    device    = "cuda" if torch.cuda.is_available() else "cpu"
    model     = model.to(device)
    return tokenizer, model, device


def chunk_text(text, tokenizer, max_tokens=900):
    words = text.split()
    chunks, current, count = [], [], 0
    for word in words:
        t = len(tokenizer.tokenize(word))
        if count + t > max_tokens:
            chunks.append(" ".join(current))
            current, count = [word], t
        else:
            current.append(word)
            count += t
    if current:
        chunks.append(" ".join(current))
    return chunks


def summarize_text(text, tokenizer, model, device,
                   max_length=150, min_length=40,
                   num_beams=4, length_penalty=2.0, no_repeat_ngram=3):
    chunks = chunk_text(text, tokenizer)
    summaries = []

    for chunk in chunks:
        if len(chunk.split()) < 20:
            continue
        inputs = tokenizer(
            chunk, return_tensors="pt",
            max_length=1024, truncation=True, padding=True
        ).to(device)
        ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            min_length=min(min_length, max_length - 10),
            num_beams=num_beams,
            length_penalty=length_penalty,
            no_repeat_ngram_size=no_repeat_ngram,
            early_stopping=True
        )
        summaries.append(tokenizer.decode(ids[0], skip_special_tokens=True))

    if len(summaries) > 1:
        combined = " ".join(summaries)
        inputs = tokenizer(
            combined, return_tensors="pt",
            max_length=1024, truncation=True, padding=True
        ).to(device)
        ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            min_length=min(min_length, max_length - 10),
            num_beams=num_beams,
            length_penalty=length_penalty,
            no_repeat_ngram_size=no_repeat_ngram,
            early_stopping=True
        )
        return tokenizer.decode(ids[0], skip_special_tokens=True)

    return summaries[0] if summaries else "Not enough content to summarize."


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:2.5rem'>✦</div>
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#6b6b8a; text-transform:uppercase;'>
            Control Panel
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">⚙ Model Settings</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6"],
        help="BART Large = accurate · DistilBART = faster"
    )

    st.markdown('<div class="sidebar-title" style="margin-top:1.2rem">📏 Output Length</div>', unsafe_allow_html=True)
    max_length = st.slider("Max Tokens", 60, 500, 150, 10)
    min_length = st.slider("Min Tokens", 10, 100, 40, 5)

    st.markdown('<div class="sidebar-title" style="margin-top:1.2rem">🎛 Generation Params</div>', unsafe_allow_html=True)
    num_beams        = st.slider("Beam Width", 1, 8, 4)
    length_penalty   = st.slider("Length Penalty", 0.5, 4.0, 2.0, 0.1)
    no_repeat_ngram  = st.slider("No-Repeat N-Gram", 1, 5, 3)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🛠 Tech Stack</div>', unsafe_allow_html=True)
    techs = ["Python","PyTorch","BART","HuggingFace","Streamlit","NLP","BeautifulSoup4","pdfplumber","python-docx","YT-Transcript"]
    tags  = " ".join([f'<span class="tech-tag active">{t}</span>' for t in techs])
    st.markdown(tags, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    device_icon = "🚀 GPU" if torch.cuda.is_available() else "💻 CPU"
    st.markdown(f"""
    <div style='font-family:"DM Mono",monospace; font-size:0.75rem;
                color:#6b6b8a; text-align:center;'>Running on {device_icon}</div>
    """, unsafe_allow_html=True)


# ─── Main Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">✦ BART · HUGGING FACE · URL · DOCS · YOUTUBE</div>
    <div class="hero-title">AI Summarizer</div>
    <div class="hero-subtitle">Text · URLs · YouTube · PDFs · DOCX · TXT</div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📝  Plain Text", "🔗  URL / YouTube", "📄  Upload Document"])

input_text   = ""
source_label = ""

# ── TAB 1: Plain Text ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.4rem;'>◈ Paste Text</div>
        """, unsafe_allow_html=True)
        t1_text = st.text_area(
            "t1", label_visibility="collapsed",
            placeholder="Paste your article, blog post, research paper, or any long-form text here...",
            height=280, key="tab1_text"
        )
        if t1_text.strip():
            w = count_words(t1_text)
            s = count_sentences(t1_text)
            st.markdown(f"""
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; margin-top:0.4rem;'>{w:,} words · {s:,} sentences</div>
            """, unsafe_allow_html=True)
        t1_btn = st.button("✦  SUMMARIZE", key="t1_btn")

    with col_out:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.4rem;'>◈ Summary Output</div>
        """, unsafe_allow_html=True)
        t1_out = st.empty()
        t1_out.markdown("""
        <div class="empty-box">
            <div style='font-size:2rem; opacity:0.2;'>✦</div>
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; letter-spacing:2px;'>AWAITING INPUT</div>
        </div>""", unsafe_allow_html=True)

    if t1_btn:
        input_text   = t1_text
        source_label = "Plain Text"
        target_out   = t1_out
        target_col   = col_out


# ── TAB 2: URL / YouTube ──────────────────────────────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_in2, col_out2 = st.columns([1, 1], gap="large")

    with col_in2:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.4rem;'>◈ Paste URL or YouTube Link</div>
        """, unsafe_allow_html=True)
        url_val = st.text_input(
            "url2", label_visibility="collapsed",
            placeholder="https://example.com/article  or  https://youtu.be/xxxxx",
            key="tab2_url"
        )

        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                    color:#6b6b8a; margin: 0.4rem 0 0.8rem;'>
            ✔ Supports: News articles · Blog posts · Wikipedia · YouTube videos
        </div>
        """, unsafe_allow_html=True)

        t2_fetch = st.button("🔍  FETCH CONTENT", key="t2_fetch")
        t2_btn   = st.button("✦  SUMMARIZE", key="t2_btn")

        if t2_fetch and url_val.strip():
            with st.spinner("Fetching content..."):
                try:
                    u = url_val.strip()
                    if not urlparse(u).scheme:
                        u = "https://" + u

                    if is_youtube_url(u):
                        fetched = extract_youtube_transcript(u)
                        st.session_state["t2_source_type"] = "YouTube"
                    else:
                        fetched = extract_text_from_url(u)
                        st.session_state["t2_source_type"] = "Web Article"

                    st.session_state["t2_text"] = fetched
                    st.session_state["t2_url"]  = u
                    st.success(f"✅ Fetched {count_words(fetched):,} words  [{st.session_state['t2_source_type']}]")
                except Exception as e:
                    st.error(f"❌ {e}")

        if "t2_text" in st.session_state:
            icon    = "▶" if st.session_state.get("t2_source_type") == "YouTube" else "🔗"
            preview = st.session_state["t2_text"][:600] + " ..."
            st.markdown(f"""
            <div class="source-badge">{icon} {st.session_state.get('t2_url','')[:55]}</div>
            <div class="extracted-box">{preview}</div>
            """, unsafe_allow_html=True)
            w = count_words(st.session_state["t2_text"])
            st.markdown(f"""
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; margin-top:0.3rem;'>{w:,} words extracted</div>
            """, unsafe_allow_html=True)

    with col_out2:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.4rem;'>◈ Summary Output</div>
        """, unsafe_allow_html=True)
        t2_out = st.empty()
        t2_out.markdown("""
        <div class="empty-box">
            <div style='font-size:2rem; opacity:0.2;'>✦</div>
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; letter-spacing:2px;'>FETCH A URL FIRST</div>
        </div>""", unsafe_allow_html=True)

    if t2_btn:
        if "t2_text" not in st.session_state:
            st.warning("⚠ Please fetch a URL first using the FETCH CONTENT button.")
        else:
            input_text   = st.session_state["t2_text"]
            source_label = st.session_state.get("t2_url", "URL")
            target_out   = t2_out
            target_col   = col_out2


# ── TAB 3: Upload Document ────────────────────────────────────────────────────
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_in3, col_out3 = st.columns([1, 1], gap="large")

    with col_in3:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.6rem;'>◈ Upload Your Document</div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "upload", type=["pdf","docx","txt","md","csv"],
            label_visibility="collapsed", key="tab3_file",
            help="Supported formats: PDF · DOCX · TXT · MD · CSV"
        )

        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                    color:#6b6b8a; margin: 0.5rem 0 0.8rem;'>
            ✔ PDF &nbsp;·&nbsp; DOCX &nbsp;·&nbsp; TXT &nbsp;·&nbsp; Markdown &nbsp;·&nbsp; CSV
        </div>
        """, unsafe_allow_html=True)

        if uploaded:
            with st.spinner(f"Reading {uploaded.name}..."):
                try:
                    extracted = extract_text_from_file(uploaded)
                    st.session_state["t3_text"] = extracted
                    st.session_state["t3_name"] = uploaded.name
                    st.success(f"✅ Extracted {count_words(extracted):,} words from **{uploaded.name}**")
                except Exception as e:
                    st.error(f"❌ {e}")

        if "t3_text" in st.session_state:
            preview = st.session_state["t3_text"][:600] + " ..."
            st.markdown(f"""
            <div class="source-badge">📄 {st.session_state.get('t3_name','')}</div>
            <div class="extracted-box">{preview}</div>
            """, unsafe_allow_html=True)
            w = count_words(st.session_state["t3_text"])
            st.markdown(f"""
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; margin-top:0.3rem;'>{w:,} words extracted</div>
            """, unsafe_allow_html=True)

        t3_btn = st.button("✦  SUMMARIZE", key="t3_btn")

    with col_out3:
        st.markdown("""
        <div style='font-family:"DM Mono",monospace; font-size:0.7rem;
                    letter-spacing:3px; color:#7c6fff; text-transform:uppercase;
                    margin-bottom:0.4rem;'>◈ Summary Output</div>
        """, unsafe_allow_html=True)
        t3_out = st.empty()
        t3_out.markdown("""
        <div class="empty-box">
            <div style='font-size:2rem; opacity:0.2;'>✦</div>
            <div style='font-family:"DM Mono",monospace; font-size:0.72rem;
                        color:#6b6b8a; letter-spacing:2px;'>UPLOAD A FILE FIRST</div>
        </div>""", unsafe_allow_html=True)

    if t3_btn:
        if "t3_text" not in st.session_state:
            st.warning("⚠ Please upload a document first.")
        else:
            input_text   = st.session_state["t3_text"]
            source_label = st.session_state.get("t3_name", "Document")
            target_out   = t3_out
            target_col   = col_out3


# ─── Summarization Engine ─────────────────────────────────────────────────────
if input_text and input_text.strip():
    if count_words(input_text) < 30:
        st.warning("⚠ Content too short — need at least 30 words for a meaningful summary.")
    else:
        progress_bar = st.progress(0)
        status_text  = st.empty()

        def set_status(msg, pct):
            status_text.markdown(f"""
            <div style='font-family:"DM Mono",monospace; font-size:0.8rem;
                        color:#7c6fff; text-align:center;'>◌ {msg}</div>
            """, unsafe_allow_html=True)
            progress_bar.progress(pct)

        try:
            set_status("Loading BART model...", 15)
            tokenizer, model, device = load_model(model_choice)

            set_status("Tokenizing & chunking text...", 40)
            time.sleep(0.2)

            set_status("Generating summary with beam search...", 65)
            start   = time.time()
            summary = summarize_text(
                input_text, tokenizer, model, device,
                max_length=max_length, min_length=min_length,
                num_beams=num_beams, length_penalty=length_penalty,
                no_repeat_ngram=no_repeat_ngram
            )
            elapsed = round(time.time() - start, 2)

            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            src_icon = "▶" if "youtu" in source_label else ("📄" if source_label not in ["Plain Text","URL"] else ("🔗" if source_label == "URL" else "📝"))

            target_out.markdown(f"""
            <div class="summary-box">
                <div class="summary-label">✦ Generated Summary</div>
                <div class="summary-text">{summary}</div>
            </div>
            """, unsafe_allow_html=True)

            in_w      = count_words(input_text)
            out_w     = count_words(summary)
            reduction = round((1 - out_w / max(in_w, 1)) * 100, 1)

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-number">{in_w:,}</div>
                    <div class="stat-label">Input Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{out_w}</div>
                    <div class="stat-label">Summary Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reduction}%</div>
                    <div class="stat-label">Reduction</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{elapsed}s</div>
                    <div class="stat-label">Inference Time</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="⬇  Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error: {str(e)}")