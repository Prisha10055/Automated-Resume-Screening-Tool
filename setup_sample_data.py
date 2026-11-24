import os
import json
from docx import Document


def create_sample_environment():
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # 1. Create Job Description
    jd_text = """
    Job Title: Junior Data & AI Analyst
    Location: Pune / Hybrid
    Experience: 1-3 Years

    About the Role:
    We are looking for a detail-oriented Junior Data & AI Analyst to build automated data pipelines,
    develop NLP/ML models, and create executive dashboards.

    Key Responsibilities:
    - Write clean, modular Python scripts for data preprocessing and automation.
    - Query and transform relational datasets using SQL and Pandas.
    - Build and evaluate machine learning and NLP classification models using Scikit-learn.
    - Visualize business KPIs using Power BI or Streamlit dashboards.
    - Collaborate via Git and deploy lightweight REST APIs using FastAPI.

    Required Skills (Must-Have):
    Python, SQL, Pandas, Scikit-learn, Git

    Preferred Skills (Nice-to-Have):
    NLP, TF-IDF, FastAPI, Streamlit, Power BI, Docker
    """
    with open("data/job_description.txt", "w", encoding="utf-8") as f:
        f.write(jd_text.strip())

    # 2. Create Skills Configuration JSON
    skills_config = {
        "job_title": "Junior Data & AI Analyst",
        "min_experience_years": 1.0,
        "shortlist_threshold": 65.0,
        "review_threshold": 45.0,
        "must_have_skills": [
            "python",
            "sql",
            "pandas",
            "scikit-learn",
            "git",
        ],
        "nice_to_have_skills": [
            "nlp",
            "tf-idf",
            "fastapi",
            "streamlit",
            "power bi",
            "docker",
            "numpy",
            "regex",
        ],
    }
    with open("data/skills_config.json", "w", encoding="utf-8") as f:
        json.dump(skills_config, f, indent=4)

    # 3. Create 5 Diverse Sample Resumes
    resumes_data = {
        "candidate_01_arjun_sharma.txt": """
            ARJUN SHARMA
            Email: arjun.sharma@example.com | Phone: +91-9876543210 | Pune, India
            Summary: Data Analyst with 2.5 years of experience in Python, SQL, and NLP pipelines.
            Skills: Python, SQL, Pandas, NumPy, Scikit-learn, NLP, TF-IDF, Streamlit, FastAPI, Git, Power BI.
            Experience:
            - Data Analyst at FinTech Corp (2 years): Automated ETL workflows using Python and Pandas, reducing reporting time by 60%. Built customer ticket classifiers using Scikit-learn and TF-IDF.
            - Junior Analyst (0.5 years): Created SQL queries and Power BI executive dashboards.
            Education: B.Tech in Computer Engineering (2024)
        """,
        "candidate_02_priya_patel.txt": """
            PRIYA PATEL
            Email: priya.patel@example.com | Mumbai, India
            Summary: Machine Learning Engineer with 2 years of experience building predictive analytics and REST APIs.
            Skills: Python, Pandas, NumPy, Scikit-learn, Git, FastAPI, Docker, Regex, NLP.
            Experience:
            - Associate ML Engineer (2 years): Developed document similarity engines and deployed FastAPI services inside Docker containers.
            Education: B.E. in Information Technology (2024)
        """,
        "candidate_03_rohan_verma.txt": """
            ROHAN VERMA
            Email: rohan.v@example.com | Bengaluru, India
            Summary: Business Intelligence Developer with 3 years of experience in reporting and database querying.
            Skills: SQL, Power BI, Excel, Python, Pandas, Tableau.
            Experience:
            - BI Developer (3 years): Designed complex SQL stored procedures and Power BI dashboards for sales forecasting. Used Python and Pandas for data cleaning.
            Education: B.Sc in Statistics (2023)
        """,
        "candidate_04_sneha_kulkarni.txt": """
            SNEHA KULKARNI
            Email: sneha.k@example.com | Karad, India
            Summary: Final-year Engineering student with strong internship experience in Python automation and ML.
            Skills: Python, Pandas, NumPy, Scikit-learn, SQL, Git, Streamlit, Matplotlib.
            Experience:
            - Data Science Intern (1 year): Built a predictive maintenance model in Scikit-learn and presented results via Streamlit. Managed version control using Git.
            Education: B.Tech in Mechanical Engineering with Minor in AI (2026)
        """,
        "candidate_05_vikram_singh.txt": """
            VIKRAM SINGH
            Email: vikram.singh@example.com | Delhi, India
            Summary: Frontend Web Developer with 2 years of experience building responsive web interfaces.
            Skills: HTML, CSS, JavaScript, React, Next.js, Tailwind CSS, Git, Figma.
            Experience:
            - Frontend Developer (2 years): Built e-commerce UI components in React and Next.js. Collaborated with backend teams using Git.
            Education: BCA (2024)
        """,
    }

    for filename, content in resumes_data.items():
        with open(os.path.join("resumes", filename), "w", encoding="utf-8") as f:
            f.write(content.strip())

    # 4. Also create 1 DOCX resume to verify Word document parsing
    doc = Document()
    doc.add_heading("ANANYA DESHMUKH", 0)
    doc.add_paragraph("Email: ananya.d@example.com | Phone: +91-9123456789 | Pune, India")
    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(
        "AI & NLP Developer with 1.5 years of experience in text classification, Python scripting, and SQL analytics."
    )
    doc.add_heading("Technical Skills", level=1)
    doc.add_paragraph(
        "Python, SQL, Pandas, Scikit-learn, Git, NLP, TF-IDF, Streamlit, Regex"
    )
    doc.add_heading("Work Experience", level=1)
    doc.add_paragraph(
        "NLP Associate (1.5 years): Automated resume and invoice parsing using Python, Regex, and Scikit-learn."
    )
    doc.save("resumes/candidate_06_ananya_deshmukh.docx")

    print("✅ Sample environment created: 6 resumes (5 .txt, 1 .docx), JD, and skills_config.json!")


if __name__ == "__main__":
    create_sample_environment()
