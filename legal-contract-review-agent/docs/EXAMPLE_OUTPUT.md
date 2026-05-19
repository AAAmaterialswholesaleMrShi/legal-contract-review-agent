# Example Output

## Terminal Output

When running `python src/main.py --contract data/sample_contract.pdf`:

```
[Supervisor] Starting contract review pipeline for: data/sample_contract.pdf
[Parsing Agent] Extracted 23 pages, 14 tables.
[Extraction Agent] Identified 41 clauses in 12 categories.
[Supervisor] Dispatching Risk Analysis Agent...
[Risk Agent] Running long-chain reasoning on 41 clauses...
[Risk Agent] 3 HIGH risk, 7 MEDIUM risk, 2 LOW risk findings.
[Supervisor] Dispatching Compliance Agent...
[Compliance Agent] 2 internal policy deviations found.
[Supervisor] Dispatching Report Agent...
[Report Agent] Report saved to reports/risk_report_20260519_143022.html
[Supervisor] Pipeline finished in 8.4 minutes. Total tokens: 786,432
```

## Sample Risk Finding

```json
{
  "clause_id": "3",
  "risk_level": "HIGH",
  "score": 8,
  "reasoning_steps": [
    {
      "regulation": "GDPR_ART28",
      "check": "Processing duration must be explicitly stated (GDPR Art.28)",
      "passed": false,
      "explanation": "Clause mentions 'providing services' but does not specify a concrete duration or end date for data processing activities."
    },
    {
      "regulation": "GDPR_ART28",
      "check": "Nature and purpose of processing must be defined",
      "passed": false,
      "explanation": "Only generic 'providing services' stated; specific processing operations not enumerated."
    },
    {
      "regulation": "GDPR_ART28",
      "check": "Types of personal data must be enumerated",
      "passed": true,
      "explanation": "Clause references 'personal data' which is acceptable as a general reference."
    }
  ],
  "suggestion": "Add/modify clause to comply with: GDPR_ART28. Include an Annex specifying processing duration, nature/purpose, and data categories."
}
```

## Sample HTML Report

The generated HTML report includes:
- Color-coded risk badges (red HIGH, orange MEDIUM, green LOW)
- Expandable reasoning traces showing each step
- Compliance violation list
- Overall risk summary statistics
