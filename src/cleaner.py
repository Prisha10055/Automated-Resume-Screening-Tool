import re


def redact_pii(text: str) -> str:
    """
    Removes email addresses and phone numbers before vectorization
    to prevent personally identifiable information (PII) bias.
    """
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
    text = re.sub(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}", " ", text)
    return text


def clean_text(text: str) -> str:
    """
    Normalizes resume/JD text for NLP vectorization while preserving
    technical symbols like '+', '#', and '-' (e.g., C++, C#, Scikit-learn).
    """
    text = redact_pii(text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\-\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
