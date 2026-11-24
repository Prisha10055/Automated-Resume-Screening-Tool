import os
import json
from pathlib import Path
from typing import Dict, List
import pandas as pd

from src.parser import parse_resume_file
from src.cleaner import clean_text
from src.extractor import analyze_candidate_profile
from src.scorer import compute_tfidf_similarities, calculate_hybrid_score


def determine_status(
    final_score: float,
    missing_must_have: List[str],
    shortlist_threshold: float,
    review_threshold: float,
) -> str:
    """
    Assigns hiring recommendation based on score and must-have skill gates.
    """
    if final_score >= shortlist_threshold and len(missing_must_have) == 0:
        return "SHORTLISTED"
    elif final_score >= review_threshold:
        return "HOLD / REVIEW"
    else:
        return "REJECTED"


def run_screening_pipeline(
    resumes_dir: str = "resumes",
    jd_path: str = "data/job_description.txt",
    config_path: str = "data/skills_config.json",
    output_csv: str = "outputs/screening_report.csv",
) -> pd.DataFrame:
    """Executes the full end-to-end resume screening workflow."""
    jd_raw = Path(jd_path).read_text(encoding="utf-8")
    jd_cleaned = clean_text(jd_raw)

    with open(config_path, "r", encoding="utf-8") as f:
        config: Dict = json.load(f)

    must_have = config.get("must_have_skills", [])
    nice_to_have = config.get("nice_to_have_skills", [])
    min_exp = config.get("min_experience_years", 1.0)
    shortlist_thresh = config.get("shortlist_threshold", 65.0)
    review_thresh = config.get("review_threshold", 45.0)

    supported_exts = {".pdf", ".docx", ".txt"}
    resume_files = sorted(
        [p for p in Path(resumes_dir).iterdir() if p.suffix.lower() in supported_exts]
    )

    if not resume_files:
        raise FileNotFoundError(f"No supported resumes (.pdf, .docx, .txt) found in '{resumes_dir}'.")

    parsed_records = []
    cleaned_texts = []

    for file_path in resume_files:
        raw_text = parse_resume_file(file_path)
        cleaned = clean_text(raw_text)
        profile = analyze_candidate_profile(
            raw_text=raw_text,
            cleaned_text=cleaned,
            filename=file_path.name,
            must_have_skills=must_have,
            nice_to_have_skills=nice_to_have,
        )
        parsed_records.append(profile)
        cleaned_texts.append(cleaned)

    similarities = compute_tfidf_similarities(jd_cleaned, cleaned_texts)

    results = []
    for idx, profile in enumerate(parsed_records):
        scores = calculate_hybrid_score(
            tfidf_sim=float(similarities[idx]),
            must_have_cov=profile["must_have_coverage"],
            nice_to_have_cov=profile["nice_to_have_coverage"],
            exp_years=profile["experience_years"],
            min_exp_years=min_exp,
        )

        status = determine_status(
            final_score=scores["final_score"],
            missing_must_have=profile["missing_must_have"],
            shortlist_threshold=shortlist_thresh,
            review_threshold=review_thresh,
        )

        results.append(
            {
                "Candidate Name": profile["candidate_name"],
                "File Name": profile["file_name"],
                "Final Score (%)": scores["final_score"],
                "Status": status,
                "TF-IDF Match (%)": scores["tfidf_similarity_pct"],
                "Must-Have Match (%)": scores["must_have_pct"],
                "Experience (Yrs)": profile["experience_years"],
                "Matched Must-Have Skills": ", ".join(profile["matched_must_have"]) or "None",
                "Missing Must-Have Gaps": ", ".join(profile["missing_must_have"]) or "None",
                "Bonus Skills": ", ".join(profile["matched_nice_to_have"]) or "None",
            }
        )

    df = pd.DataFrame(results).sort_values(by="Final Score (%)", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    return df
