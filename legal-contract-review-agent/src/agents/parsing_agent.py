"""Parsing Agent - converts contract documents to raw text."""
from rich.console import Console

console = Console()


class ParsingAgent:
    def parse(self, path: str) -> str:
        ext = path.lower().split(".")[-1] if "." in path else ""

        if ext == "pdf":
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
                console.print(
                    "[yellow]pdfplumber not installed. Using mock text.[/]"
                )
            except Exception as e:
                console.print(f"[yellow]PDF parse error: {e}. Using mock text.[/]")

        elif ext == "docx":
            try:
                from docx import Document

                doc = Document(path)
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                console.print(
                    "[yellow]python-docx not installed. Using mock text.[/]"
                )
            except Exception as e:
                console.print(f"[yellow]DOCX parse error: {e}. Using mock text.[/]")

        # Mock contract text for demonstration
        return (
            "CONTRACT AGREEMENT\n\n"
            "1. Indemnification: Party A shall indemnify and hold harmless "
            "Party B against all claims arising from this agreement. "
            "Liability cap is set at $500,000.\n\n"
            "2. Payment Terms: Payment shall be made within 45 days of "
            "invoice receipt. Late payments incur 1.5% monthly interest.\n\n"
            "3. Data Processing: Processor shall process personal data "
            "on behalf of Controller for the purpose of providing services.\n\n"
            "4. Termination: Either party may terminate with 30 days "
            "written notice.\n\n"
            "5. Confidentiality: Both parties agree to maintain "
            "confidentiality of proprietary information for 3 years.\n"
        )
