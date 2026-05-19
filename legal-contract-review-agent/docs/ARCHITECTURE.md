# Architecture: Legal Contract Review Agent

## High-Level Design

The system follows a **Supervisor-orchestrated Multi-Agent Pipeline** pattern.

```
                    ┌──────────────┐
                    │  User Input   │
                    │ (PDF / DOCX)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Parsing Agent │
                    │ (Document →   │
                    │  Raw Text)    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Extraction    │
                    │ Agent         │
                    │ (Text →       │
                    │  Clauses)     │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────▼───┐  ┌─────▼──────┐    │
     │ Risk Agent  │  │ Compliance │    │
     │ (Long-chain │  │ Agent      │    │
     │  Reasoning) │  │ (Policy)   │    │
     └────────┬────┘  └─────┬──────┘    │
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼───────┐
                    │ Supervisor   │
                    │ Agent        │
                    │ (Orchestrate)│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Report Agent │
                    │ (HTML Output)│
                    └──────────────┘
```

## Agent Details

### 1. Parsing Agent
- **Input:** Contract file path (.pdf / .docx)
- **Output:** Raw text string
- **Strategy:** Uses `pdfplumber` for PDFs, `python-docx` for DOCX
- **Fallback:** Returns mock contract text for demo purposes

### 2. Extraction Agent
- **Input:** Raw text
- **Output:** `List[Clause]` with types
- **Strategy:** Regex-based clause classification across 8 clause types
- **Extensible:** Add new patterns to `CLAUSE_PATTERNS` dict

### 3. Risk Analysis Agent (Core)
- **Input:** `List[Clause]`
- **Output:** `List[RiskFinding]` with reasoning traces
- **Strategy:** Long-chain reasoning:
  1. Retrieve relevant regulations from Legal KB
  2. Decompose each regulation into atomic checks
  3. Use LLM for semantic clause-vs-check comparison
  4. Aggregate risk score across checks
  5. Generate natural language suggestions
- **Design rationale:** Not simple regex matching — uses LLM for semantic understanding of legal text

### 4. Compliance Agent
- **Input:** `List[Clause]`
- **Output:** `List[str]` policy violations
- **Strategy:** Rule-based policy checks against internal standards

### 5. Report Agent
- **Input:** Risk findings + compliance issues
- **Output:** HTML report file
- **Strategy:** Generate styled HTML with risk summaries and reasoning traces

### 6. Supervisor Agent
- **Role:** Pipeline orchestrator
- **Responsibilities:**
  - Sequential agent dispatch
  - Progress logging via Rich console
  - Error handling and retry logic
  - Report path generation

## Data Flow

```
Contract → Text → Clauses → [RiskFindings + ComplianceIssues] → HTML Report
```

## Key Design Decisions

1. **Pydantic schemas** ensure type safety across agents
2. **LLMClient abstraction** allows swapping between MiMo and OpenAI
3. **Mock mode** enables demo without API key
4. **Legal KB** is modular — can be replaced with vector DB for production
5. **Supervisor pattern** keeps agents decoupled and independently testable
