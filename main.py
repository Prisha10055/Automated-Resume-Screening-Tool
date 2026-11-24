from src.pipeline import run_screening_pipeline


def main():
    print("=" * 75)
    print("🚀 AUTOMATED RESUME SCREENING TOOL — STARTING PIPELINE")
    print("=" * 75)

    df = run_screening_pipeline()

    print("\n📊 RANKED CANDIDATE SHORTLIST REPORT:\n")
    display_cols = [
        "Rank",
        "Candidate Name",
        "Final Score (%)",
        "Status",
        "Experience (Yrs)",
        "Missing Must-Have Gaps",
    ]
    print(df[display_cols].to_string(index=False))

    shortlisted_count = (df["Status"] == "SHORTLISTED").sum()
    review_count = (df["Status"] == "HOLD / REVIEW").sum()
    rejected_count = (df["Status"] == "REJECTED").sum()

    print("\n" + "-" * 75)
    print(
        f"✅ Summary: {len(df)} Resumes Processed | "
        f"Shortlisted: {shortlisted_count} | Hold/Review: {review_count} | Rejected: {rejected_count}"
    )
    print("📁 Full detailed report saved to: outputs/screening_report.csv")
    print("=" * 75)


if __name__ == "__main__":
    main()
