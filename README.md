# 📄 Automated Resume Screening Tool

An end-to-end **Python, NLP, and HR Tech pipeline** that ingests candidate resumes (`.pdf`, `.docx`, `.txt`), extracts skills and experience, compares profiles against a Job Description using **TF-IDF + Cosine Similarity** and rule-based must-have gates, flags skill gaps, and generates ranked hiring reports via CLI, **Streamlit**, and **FastAPI**.

## ✨ Key Features
- **Multi-Format Resume Parsing:** Extracts clean text from `.pdf` (`pdfplumber`), `.docx` (`python-docx`, including tables), and `.txt` files.
- **Privacy-First Text Normalization:** Automatically redacts email addresses and phone numbers before vectorization to reduce PII bias.
- **Boundary-Safe Skill & Experience Extraction:** Uses word-boundary Regex (`\b`) to accurately detect technical skills and years of experience.
- **Hybrid Explainable Scoring:** Combines **TF-IDF + Cosine Similarity (40%)**, **Must-Have Skill Coverage (40%)**, **Nice-to-Have Skills (10%)**, and **Experience Alignment (10%)**.
- **Automated Gap Flagging:** Explicitly highlights missing mandatory skills (`Missing Must-Have Gaps`) even when overall text similarity is high.
- **Multiple Interfaces:** Run via CLI (`main.py`), interactive **Streamlit** dashboard (`app.py`), or **FastAPI** REST microservice (`api.py`).

## 🚀 Quick Start
```bash
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python setup_sample_data.py
python main.py
streamlit run app.py
```
