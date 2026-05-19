"""Extraction Agent - classifies contract text into structured clauses."""
import re
from typing import List

from models.schemas import Clause


class ExtractionAgent:
    CLAUSE_PATTERNS = {
        "indemnification": r"(?i)(indemnif|hold.?harmless)",
        "payment_terms": r"(?i)(payment|invoice|fee|compensation)",
        "data_processing": r"(?i)(data\s*process|personal\s*data|gdpr|privacy)",
        "termination": r"(?i)(terminat|cancel|renewal)",
        "confidentiality": r"(?i)(confiden|non.?disclos|nda|trade\s*secret)",
        "liability": r"(?i)(liab|warrant|disclaim)",
        "governing_law": r"(?i)(govern\s*law|jurisdict|arbitrat|venue)",
        "force_majeure": r"(?i)(force\s*majeure|act\s*of\s*god)",
    }

    def extract(self, text: str) -> List[Clause]:
        lines = text.split("\n")
        clauses = []
        clause_id = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 15:
                continue

            for clause_type, pattern in self.CLAUSE_PATTERNS.items():
                if re.search(pattern, line):
                    clause_id += 1
                    clauses.append(Clause(
                        id=str(clause_id),
                        type=clause_type,
                        text=line,
                        page=max(1, (i // 40) + 1),
                    ))
                    break

        return clauses
