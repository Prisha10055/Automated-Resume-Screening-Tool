import tempfile
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from src.parser import parse_resume_file
from src.cleaner import clean_text
from src.extractor import analyze_candidate_profile
from src.scorer import compute_tfidf_similarities, calculate_hybrid_score
from src.pipeline import determine_status

app = FastAPI(title="Automated Resume Screening API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Automated Resume Screening Tool"}


@app.post("/screen")
async def screen_resumes(
    jd_text: str = Form(...),
    must_have_skills: str = Form("python,sql,pandas,scikit-learn,git"),
    nice_to_have_skills: str = Form("nlp,tf-idf,fastapi,streamlit"),
    min_experience_years: float = Form(1.0),
    files: List[UploadFile] = File(...),
):
    must_list = [s.strip() for s in must_have_skills.split(",") if s.strip()]
    nice_list = [s.strip() for s in nice_to_have_skills.split(",") if s.strip()]
    jd_cleaned = clean_text(jd_text)

    profiles = []
    cleaned_texts = []

    for f in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.filename).suffix) as tmp:
            tmp.write(await f.read())
            tmp_path = tmp.name
        raw = parse_resume_file(tmp_path)
        cleaned = clean_text(raw)
        profiles.append(analyze_candidate_profile(raw, cleaned, f.filename, must_list, nice_list))
        cleaned_texts.append(cleaned)

    sims = compute_tfidf_similarities(jd_cleaned, cleaned_texts)
    ranked = []
    for idx, p in enumerate(profiles):
        sc = calculate_hybrid_score(
            float(sims[idx]), p["must_have_coverage"], p["nice_to_have_coverage"], p["experience_years"], min_experience_years
        )
        status = determine_status(sc["final_score"], p["missing_must_have"], 65.0, 45.0)
        ranked.append({**p, **sc, "status": status})

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return {"total_candidates": len(ranked), "results": ranked}
