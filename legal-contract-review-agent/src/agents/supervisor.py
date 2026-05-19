"""Supervisor Agent - orchestrates the multi-agent pipeline."""
import os
from datetime import datetime

from rich.console import Console

from agents.parsing_agent import ParsingAgent
from agents.extraction_agent import ExtractionAgent
from agents.risk_agent import RiskAnalysisAgent
from agents.compliance_agent import ComplianceAgent
from agents.report_agent import ReportAgent

console = Console()


class SupervisorAgent:
    def __init__(self):
        self.parsing = ParsingAgent()
        self.extraction = ExtractionAgent()
        self.risk = RiskAnalysisAgent()
        self.compliance = ComplianceAgent()
        self.report = ReportAgent()

    def run_pipeline(self, contract_path: str) -> str:
        contract_name = os.path.basename(contract_path)

        # Step 1: Parse document
        console.print("[blue][Supervisor] Dispatching Parsing Agent...[/]")
        text = self.parsing.parse(contract_path)
        console.print(f"[dim][Parsing Agent] Extracted {len(text)} characters.[/]")

        # Step 2: Extract clauses
        console.print("[blue][Supervisor] Dispatching Extraction Agent...[/]")
        clauses = self.extraction.extract(text)
        console.print(
            f"[dim][Extraction Agent] Identified {len(clauses)} clauses "
            f"in {len(set(c.type for c in clauses))} categories.[/]"
        )

        # Step 3: Risk analysis (long-chain reasoning)
        console.print("[blue][Supervisor] Dispatching Risk Analysis Agent...[/]")
        console.print("[dim][Risk Agent] Running long-chain reasoning on clauses...[/]")
        risk_findings = self.risk.analyze(clauses)
        high_risks = sum(1 for f in risk_findings if f.risk_level == "HIGH")
        med_risks = sum(1 for f in risk_findings if f.risk_level == "MEDIUM")
        console.print(
            f"[dim][Risk Agent] {high_risks} HIGH risk, {med_risks} MEDIUM risk "
            f"findings.[/]"
        )

        # Step 4: Compliance check
        console.print("[blue][Supervisor] Dispatching Compliance Agent...[/]")
        compliance_issues = self.compliance.check(clauses)
        console.print(
            f"[dim][Compliance Agent] {len(compliance_issues)} "
            f"internal policy deviations.[/]"
        )

        # Step 5: Generate report
        console.print("[blue][Supervisor] Dispatching Report Agent...[/]")
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/risk_report_{timestamp}.html"
        self.report.generate(
            contract_name, risk_findings, compliance_issues, report_path
        )

        return report_path
