from pathlib import Path
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: Path) -> str:
    """Extracts text page-by-page from a PDF file using pdfplumber."""
    text_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


def extract_text_from_docx(file_path: Path) -> str:
    """Extracts paragraphs and table text from a DOCX file."""
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            row_text = " ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                paragraphs.append(row_text)
    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: Path) -> str:
    """Reads plain text files safely with UTF-8 fallback."""
    return file_path.read_text(encoding="utf-8", errors="ignore")


def parse_resume_file(file_path: str | Path) -> str:
    """
    Unified entry point to extract raw text from .pdf, .docx, or .txt resumes.
    Raises ValueError for unsupported extensions.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".txt":
        return extract_text_from_txt(path)
    else:
        raise ValueError(f"Unsupported file format '{ext}' for file: {path.name}")
