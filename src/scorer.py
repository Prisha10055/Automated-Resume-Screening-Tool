from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_similarities(cleaned_jd: str, cleaned_resumes: List[str]) -> np.ndarray:
    """
    Fits a TF-IDF Vectorizer across the Job Description and all resumes jointly,
    then computes Cosine Similarity between the JD vector and each resume vector.
    """
    if not cleaned_resumes:
        return np.array([])

    corpus = [cleaned_jd] + cleaned_resumes
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
    return similarities


def calculate_hybrid_score(
    tfidf_sim: float,
    must_have_cov: float,
    nice_to_have_cov: float,
    exp_years: float,
    min_exp_years: float,
) -> Dict[str, float]:
    """
    Combines semantic TF-IDF similarity with deterministic HR skill & experience rules.
    Weights:
      - 40% TF-IDF Semantic Similarity
      - 40% Must-Have Skill Coverage
      - 10% Nice-to-Have Skill Coverage
      - 10% Experience Alignment
    """
    exp_ratio = min(1.0, exp_years / max(0.5, min_exp_years)) if min_exp_years > 0 else 1.0

    raw_score = (
        0.40 * tfidf_sim
        + 0.40 * must_have_cov
        + 0.10 * nice_to_have_cov
        + 0.10 * exp_ratio
    )
    final_score_pct = round(raw_score * 100, 2)

    return {
        "tfidf_similarity_pct": round(tfidf_sim * 100, 2),
        "must_have_pct": round(must_have_cov * 100, 2),
        "nice_to_have_pct": round(nice_to_have_cov * 100, 2),
        "final_score": final_score_pct,
    }
