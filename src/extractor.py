import re
from typing import Dict, List


def extract_candidate_name(raw_text: str, fallback_filename: str) -> str:
    """Extracts candidate name from the first non-empty line or cleans filename."""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if lines and len(lines[0].split()) <= 4 and not any(ch.isdigit() for ch in lines[0]):
        return lines[0].title()
    clean_name = re.sub(r"^candidate_\d+_", "", fallback_filename.rsplit(".", 1)[0])
    return clean_name.replace("_", " ").title()


def extract_experience_years(raw_text: str) -> float:
    """
    Uses Regex to detect years of experience mentioned in the resume
    (e.g., '2.5 years', '3+ yrs', '1 year').
    """
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)\b", raw_text.lower())
    if not matches:
        return 0.0
    return max(float(val) for val in matches)


def match_skills(cleaned_text: str, skill_list: List[str]) -> List[str]:
    """
    Performs boundary-safe Regex matching so short skills like 'git' or 'sql'
    do not falsely match inside unrelated words.
    """
    matched = []
    for skill in skill_list:
        skill_lower = skill.lower().strip()
        escaped = re.escape(skill_lower)
        pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
        if re.search(pattern, cleaned_text):
            matched.append(skill_lower)
    return sorted(list(set(matched)))


def analyze_candidate_profile(
    raw_text: str,
    cleaned_text: str,
    filename: str,
    must_have_skills: List[str],
    nice_to_have_skills: List[str],
) -> Dict:
    """Extracts structured candidate attributes and identifies must-have skill gaps."""
    name = extract_candidate_name(raw_text, filename)
    exp_years = extract_experience_years(raw_text)

    must_have_norm = [s.lower().strip() for s in must_have_skills]
    nice_to_have_norm = [s.lower().strip() for s in nice_to_have_skills]

    matched_must = match_skills(cleaned_text, must_have_norm)
    missing_must = sorted(list(set(must_have_norm) - set(matched_must)))
    matched_nice = match_skills(cleaned_text, nice_to_have_norm)

    return {
        "candidate_name": name,
        "file_name": filename,
        "experience_years": exp_years,
        "matched_must_have": matched_must,
        "missing_must_have": missing_must,
        "matched_nice_to_have": matched_nice,
        "must_have_coverage": len(matched_must) / max(1, len(must_have_norm)),
        "nice_to_have_coverage": len(matched_nice) / max(1, len(nice_to_have_norm)),
    }
