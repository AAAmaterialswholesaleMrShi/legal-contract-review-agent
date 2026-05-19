"""Data schemas used across agents (Pydantic models)."""
from typing import List, Optional

from pydantic import BaseModel


class Clause(BaseModel):
    id: str
    type: str  # e.g., "indemnification", "payment_terms"
    text: str
    page: int = 1


class ReasoningStep(BaseModel):
    regulation: str
    check: str
    passed: bool
    explanation: str


class RiskFinding(BaseModel):
    clause_id: str
    risk_level: str  # "HIGH", "MEDIUM", "LOW"
    score: int
    reasoning_steps: List[ReasoningStep]
    suggestion: str


class ContractReport(BaseModel):
    contract_name: str
    risk_findings: List[RiskFinding]
    compliance_issues: List[str]
    summary: str
