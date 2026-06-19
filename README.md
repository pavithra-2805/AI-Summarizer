# 🚀 AI Text Summarizer

An intelligent, AI-powered text summarization application built with **Streamlit**, **PyTorch**, and **Facebook's BART Large CNN** model from Hugging Face.

The application allows users to summarize **plain text, web articles, YouTube videos, and uploaded documents** through a modern and interactive interface while providing customizable summarization settings.

---

## ✨ Features

### 📝 Text Summarization
- Summarize long articles, reports, blogs, essays, and research papers.
- Generates concise, coherent, and meaningful summaries using the BART transformer model.

### 🌐 URL Summarization
- Extracts textual content directly from web pages.
- Removes advertisements, navigation menus, scripts, and unnecessary page elements before summarization.

### ▶️ YouTube Video Summarization
- Fetches captions/transcripts from YouTube videos.
- Automatically converts transcripts into readable summaries.
- Supports videos with available subtitles.

### 📄 Document Summarization
Upload and summarize documents in multiple formats:

- PDF (.pdf)
- Microsoft Word (.docx)
- Text (.txt)
- Markdown (.md)
- CSV (.csv)

### ⚙️ Customizable AI Parameters

Users can customize:

- Maximum summary length
- Minimum summary length
- Beam search width
- Length penalty
- No-repeat n-gram size

This allows balancing between summary quality, speed, and compression ratio.

### 📊 Analytics Dashboard

After every summary the application displays:

- Input word count
- Output word count
- Compression percentage
- Inference time
- Processing device (CPU/GPU)

### 💾 Export Results

- Download summaries as text files.
- Easy sharing and offline storage.

---

# 🖥 User Interface

The application includes three major modules:

### 📝 Plain Text

Paste any text directly into the editor and generate a summary.

---

### 🔗 URL & YouTube

Paste:

- News article URLs
- Blog links
- Wikipedia pages
- YouTube video links

The application automatically extracts the content before summarizing.

---

### 📄 Upload Document

Supports:

- PDF
- DOCX
- TXT
- Markdown
- CSV

The uploaded document is parsed and summarized automatically.

---

# 🧠 AI Model

The project uses Facebook's pretrained transformer model:

**facebook/bart-large-cnn**

Advantages:

- State-of-the-art abstractive summarization
- Generates human-like summaries
- Handles long documents
- Produces coherent paragraphs

Framework:

- Hugging Face Transformers

Backend:

- PyTorch

---

# 🏗 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Deep Learning | PyTorch |
| NLP | Hugging Face Transformers |
| Model | Facebook BART Large CNN |
| HTML Parsing | BeautifulSoup4 |
| PDF Processing | pdfplumber |
| Word Documents | python-docx |
| HTTP Requests | Requests |
| YouTube Captions | youtube-transcript-api |

---

# 📂 Project Structure

```text
AI-SUMMARIZER/
│
├── app.py
├── requirements.txt
├── README.md
├── assets/
│     ├── screenshots/
│     └── logo.png
└── sample_files/
```

---

# ⚙ Installation

## 1. Clone Repository

```bash
git clone https://github.com/Narasimha2308/AI-SUMMARIZER.git
```

```bash
cd AI-SUMMARIZER
```

---

## 2. Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install streamlit transformers torch requests beautifulsoup4 pdfplumber python-docx youtube-transcript-api
```

---

# ▶ Running the Application

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 📖 How to Use

## Option 1 — Plain Text

1. Open the **Plain Text** tab.
2. Paste your text.
3. Click **Summarize**.

---

## Option 2 — URL / YouTube

1. Open the **URL / YouTube** tab.
2. Paste a webpage or YouTube URL.
3. Click **Fetch Content**.
4. Click **Summarize**.

---

## Option 3 — Upload Documents

1. Open **Upload Document**.
2. Select a supported file.
3. Click **Summarize**.

---

# 📈 Output Metrics

After summarization, the application displays:

- Original word count
- Summary word count
- Compression percentage
- Processing time
- Summary download option

---

# 🖼 Screenshots

Add screenshots here.

Example:

```
assets/screenshots/home.png
assets/screenshots/url.png
assets/screenshots/upload.png
```

---

# 🚀 Future Enhancements

- Multiple AI models (T5, PEGASUS, FLAN-T5)
- Multilingual summarization
- OCR support for scanned PDFs
- Audio summarization
- Video summarization
- AI-powered key insights
- Keyword extraction
- Bullet-point summaries
- Dark/Light theme switch
- Chat with uploaded documents
- Cloud deployment
- User authentication
- Summary history

---

# ⚡ Performance

- GPU acceleration using CUDA (if available)
- Automatic CPU fallback
- Cached AI model loading
- Efficient chunk-based summarization for long documents

---

# 📌 Limitations

- First launch downloads the BART model (~1.6 GB).
- Very large PDFs require additional processing time.
- YouTube videos must have available captions.
- Some websites restrict automated content extraction.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is released under the **MIT License**.

---

# 👨‍💻 Author

**Lakshmi Pavithra Korukonda**

GitHub: https://github.com/pavithra-2805

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub to support future development.
