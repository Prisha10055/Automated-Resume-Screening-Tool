import tempfile
from pathlib import Path
import streamlit as st
import pandas as pd

from src.parser import parse_resume_file
from src.cleaner import clean_text
from src.extractor import analyze_candidate_profile
from src.scorer import compute_tfidf_similarities, calculate_hybrid_score
from src.pipeline import determine_status

st.set_page_config(page_title="Automated Resume Screening Tool", page_icon="📄", layout="wide")

st.title("📄 Automated Resume Screening & ATS Ranking Dashboard")
st.markdown(
    "Upload candidate resumes (`.pdf`, `.docx`, `.txt`), configure job requirements, and generate explainable rankings."
)

with st.sidebar:
    st.header("⚙️ Screening Thresholds")
    shortlist_thresh = st.slider("Shortlist Threshold (%)", 40, 95, 65)
    review_thresh = st.slider("Hold / Review Threshold (%)", 20, 75, 45)
    min_exp = st.number_input("Minimum Experience (Years)", min_value=0.0, max_value=15.0, value=1.0, step=0.5)

default_jd = Path("data/job_description.txt").read_text(encoding="utf-8") if Path("data/job_description.txt").exists() else ""
default_must = "python, sql, pandas, scikit-learn, git"
default_nice = "nlp, tf-idf, fastapi, streamlit, power bi, docker"

col1, col2 = st.columns([1.3, 1])

with col1:
    jd_input = st.text_area("📋 Job Description (JD)", value=default_jd, height=240)

with col2:
    must_have_input = st.text_input("🔴 Must-Have Skills (comma-separated)", value=default_must)
    nice_to_have_input = st.text_input("🟢 Nice-to-Have Skills (comma-separated)", value=default_nice)
    uploaded_files = st.file_uploader(
        "📂 Upload Resumes (PDF, DOCX, TXT) — Leave empty to use sample /resumes folder",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

if st.button("🚀 Run Resume Screening", type="primary"):
    must_have_list = [s.strip() for s in must_have_input.split(",") if s.strip()]
    nice_to_have_list = [s.strip() for s in nice_to_have_input.split(",") if s.strip()]
    jd_cleaned = clean_text(jd_input)

    records = []
    cleaned_texts = []

    if uploaded_files:
        for uf in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uf.name).suffix) as tmp:
                tmp.write(uf.read())
                tmp_path = tmp.name
            raw_text = parse_resume_file(tmp_path)
            cleaned = clean_text(raw_text)
            profile = analyze_candidate_profile(raw_text, cleaned, uf.name, must_have_list, nice_to_have_list)
            records.append(profile)
            cleaned_texts.append(cleaned)
    else:
        for file_path in sorted(Path("resumes").iterdir()):
            if file_path.suffix.lower() in {".pdf", ".docx", ".txt"}:
                raw_text = parse_resume_file(file_path)
                cleaned = clean_text(raw_text)
                profile = analyze_candidate_profile(raw_text, cleaned, file_path.name, must_have_list, nice_to_have_list)
                records.append(profile)
                cleaned_texts.append(cleaned)

    if not records:
        st.error("No resumes found! Upload files or run `python setup_sample_data.py` first.")
    else:
        sims = compute_tfidf_similarities(jd_cleaned, cleaned_texts)
        rows = []
        for i, p in enumerate(records):
            sc = calculate_hybrid_score(
                float(sims[i]), p["must_have_coverage"], p["nice_to_have_coverage"], p["experience_years"], min_exp
            )
            status = determine_status(sc["final_score"], p["missing_must_have"], shortlist_thresh, review_thresh)
            rows.append(
                {
                    "Candidate Name": p["candidate_name"],
                    "Final Score (%)": sc["final_score"],
                    "Status": status,
                    "TF-IDF Match (%)": sc["tfidf_similarity_pct"],
                    "Must-Have Match (%)": sc["must_have_pct"],
                    "Exp (Yrs)": p["experience_years"],
                    "Matched Must-Have": ", ".join(p["matched_must_have"]) or "None",
                    "Missing Must-Have Gaps": ", ".join(p["missing_must_have"]) or "None",
                    "Bonus Skills": ", ".join(p["matched_nice_to_have"]) or "None",
                }
            )

        df = pd.DataFrame(rows).sort_values(by="Final Score (%)", ascending=False).reset_index(drop=True)
        df.insert(0, "Rank", df.index + 1)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Resumes", len(df))
        m2.metric("Shortlisted", int((df["Status"] == "SHORTLISTED").sum()))
        m3.metric("Hold / Review", int((df["Status"] == "HOLD / REVIEW").sum()))
        m4.metric("Top Score", f"{df['Final Score (%)'].max()}%")

        st.subheader("🏆 Candidate Ranking & Gap Analysis")
        st.dataframe(df, use_container_width=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Ranked CSV Report",
            data=csv_bytes,
            file_name="screening_report.csv",
            mime="text/csv",
        )
