"""PDF parsing utilities for contract documents."""


def extract_text_from_pdf(path: str) -> str:
    try:
        import pdfplumber

        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n".join(text_parts)
    except ImportError:
        raise ImportError("pdfplumber is required. Run: pip install pdfplumber")


def extract_tables_from_pdf(path: str) -> list:
    try:
        import pdfplumber

        all_tables = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                all_tables.extend(tables)
        return all_tables
    except ImportError:
        raise ImportError("pdfplumber is required. Run: pip install pdfplumber")
