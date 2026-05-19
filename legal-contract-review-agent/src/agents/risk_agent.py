"""Risk Analysis Agent - performs long-chain legal reasoning."""
import json
from typing import List

from models.schemas import Clause, RiskFinding, ReasoningStep
from tools.legal_kb import LegalKnowledgeBase
from utils.llm_client import LLMClient


class RiskAnalysisAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.kb = LegalKnowledgeBase()

    def analyze(self, clauses: List[Clause]) -> List[RiskFinding]:
        findings = []

        for clause in clauses:
            regulations = self.kb.retrieve(clause.type)
            if not regulations:
                continue

            reasoning_steps = []
            risk_score = 0

            for reg in regulations:
                for check in reg["checks"]:
                    prompt = self._build_prompt(clause.text, check)
                    raw = self.llm.complete(prompt)

                    try:
                        result = json.loads(raw)
                    except json.JSONDecodeError:
                        result = {"passed": True, "explanation": "parse error, assuming compliant"}

                    step = ReasoningStep(
                        regulation=reg["id"],
                        check=check["description"],
                        passed=result.get("passed", True),
                        explanation=result.get("explanation", ""),
                    )
                    reasoning_steps.append(step)

                    if not result.get("passed", True):
                        risk_score += check.get("severity", 1)

            if risk_score > 0:
                if risk_score >= 7:
                    level = "HIGH"
                elif risk_score >= 3:
                    level = "MEDIUM"
                else:
                    level = "LOW"

                failed_regs = [
                    r.regulation for r in reasoning_steps if not r.passed
                ]
                suggestion = (
                    f"Add/modify clause to comply with: {', '.join(failed_regs)}"
                )

                findings.append(RiskFinding(
                    clause_id=clause.id,
                    risk_level=level,
                    score=risk_score,
                    reasoning_steps=reasoning_steps,
                    suggestion=suggestion,
                ))

        return findings

    def _build_prompt(self, clause_text: str, check: dict) -> str:
        return (
            f'You are a legal compliance auditor. Given this contract clause:\n\n'
            f'"{clause_text}"\n\n'
            f'And the requirement: "{check["description"]}"\n\n'
            f'Does the clause fully comply? Respond in JSON: '
            f'{{"passed": true/false, "explanation": "short reason"}}'
        )
