"""Compliance Agent - checks clauses against internal policies."""
from typing import List

from models.schemas import Clause


class ComplianceAgent:
    INTERNAL_POLICIES = [
        {
            "id": "POL-001",
            "description": "Payment terms must not exceed 30 days",
            "check": lambda c: "45" not in c.text if c.type == "payment_terms" else True,
        },
        {
            "id": "POL-002",
            "description": "Confidentiality period must be at least 5 years",
            "check": lambda c: "3 year" not in c.text.lower() if c.type == "confidentiality" else True,
        },
    ]

    def check(self, clauses: List[Clause]) -> List[str]:
        issues = []

        for clause in clauses:
            for policy in self.INTERNAL_POLICIES:
                try:
                    if not policy["check"](clause):
                        issues.append(
                            f"Policy violation ({policy['id']}): "
                            f"{policy['description']} — Clause [{clause.id}] {clause.type}"
                        )
                except Exception:
                    continue

        return issues
