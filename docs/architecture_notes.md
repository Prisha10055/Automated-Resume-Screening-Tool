# Architecture & Design Decisions

1. **Joint TF-IDF Fitting:** Fitting `TfidfVectorizer` jointly on `[cleaned_jd] + cleaned_resumes` guarantees aligned feature dimensions and accurate IDF weighting.
2. **Hybrid Scoring Formula:**
   - 40% TF-IDF Cosine Similarity (unigrams + bigrams)
   - 40% Must-Have Skill Coverage
   - 10% Nice-to-Have Skill Coverage
   - 10% Experience Ratio
3. **Bias Mitigation:** PII (emails and phone numbers) is redacted prior to vectorization.
