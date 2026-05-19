# Multi-Agent Flow

## Overview

The system uses a **Supervisor-orchestrated pipeline** with 6 specialized agents:

```
Supervisor → Parsing → Extraction → Risk Analysis → Compliance → Report
```

## Detailed Agent Flow

### Step 1: Document Parsing
```
Agent: ParsingAgent
Input:  contract.pdf
Output: Raw text string
Time:   ~30 seconds
```

The Parsing Agent handles both PDF and DOCX formats. It extracts all textual content including tables and preserves the reading order.

### Step 2: Clause Extraction
```
Agent: ExtractionAgent
Input:  Raw text
Output: List[Clause] with types
Time:   ~5 seconds
```

Uses regex patterns to identify and classify clauses. Currently supports 8 clause types including indemnification, payment terms, data processing, termination, confidentiality, liability, governing law, and force majeure.

### Step 3: Risk Analysis (Long-Chain Reasoning)
```
Agent: RiskAnalysisAgent
Input:  List[Clause]
Output: List[RiskFinding]
Time:   ~5-8 minutes (LLM-dependent)
```

This is the core intelligence of the system. For each clause:

1. **Retrieve** → Query Legal KB for applicable regulations
2. **Decompose** → Break each regulation into atomic compliance checks
3. **Compare** → Use LLM to semantically compare clause text vs each check
4. **Score** → Aggregate severity-weighted risk score
5. **Explain** → Generate natural language reasoning trace

### Step 4: Compliance Check
```
Agent: ComplianceAgent
Input:  List[Clause]
Output: List[str] policy violations
Time:   < 1 second
```

Rule-based checks against internal corporate policies (e.g., payment terms limits, confidentiality duration requirements).

### Step 5: Report Generation
```
Agent: ReportAgent
Input:  RiskFindings + ComplianceIssues
Output: HTML report file
Time:   ~1 second
```

Generates a styled, interactive HTML report with:
- Risk severity summary (HIGH/MEDIUM/LOW badges)
- Detailed reasoning traces for each finding
- Compliance issue list
- Suggested remediations

## Example Reasoning Trace

For a data processing clause missing DPA annexes:

```
[Step 1] Found matching regulation: GDPR Article 28(3)
[Step 2] Obligations required: (a) data subjects, (b) duration,
         (c) nature/purpose, (d) type of data, (e) processor obligations
[Step 3] Clause fulfills (a),(d),(e) but lacks explicit statement
         of (b) duration and (c) purpose
[Step 4] Risk: HIGH — missing mandatory processor agreement details
[Step 5] Suggestion: Add an Annex with processing duration and
         specific purposes
```

## Parallelization Potential

While the current implementation runs sequentially, Risk Analysis and Compliance agents can run in parallel since they share no dependencies — both consume the same `List[Clause]` input.

## Error Handling

- Parsing failures fall back to mock contract text
- LLM JSON parse errors default to "compliant" (fail-safe)
- Supervisor handles agent exceptions and continues pipeline
