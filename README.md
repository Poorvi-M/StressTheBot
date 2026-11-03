# StressTheBot

**Push medical AI to its limits. Expose where safety breaks.**

StressTheBot is a clinical AI safety stress-testing platform designed to evaluate how Large Language Models (LLMs) respond to clinical scenarios involving potential patient safety risks.

Instead of relying only on overall model accuracy or general-purpose AI evaluation, StressTheBot examines individual model responses against sourced clinical safety rules. It aims to identify potentially unsafe recommendations, missing safety warnings and gaps in expected clinical behaviour.

> **Disclaimer:** StressTheBot is a research and evaluation prototype. It is not intended for clinical diagnosis, treatment recommendations or real-world medical decision-making. Its automated evaluation results require human review.

## Key Features

- **Synthetic Clinical Scenarios:** Generate configurable patient scenarios using clinical parameters and constraints.
- **Parameter Sweeps:** Vary patient characteristics to investigate how model responses change across different scenarios.
- **Multi-Model Evaluation:** Execute scenarios against supported LLM providers and compare their responses.
- **Source-Linked Clinical Rules:** Evaluate responses against structured safety rules containing references to clinical guidelines.
- **Automated Response Extraction:** Extract relevant recommendations, warnings, monitoring suggestions and safety-related statements.
- **Rule-Based Evaluation:** Use deterministic pattern-based checks to identify potential violations and missing expected behaviours.
- **Risk Analysis:** Organise evaluation results by rule, severity, model and evaluation status.
- **Model Comparison:** Compare model responses and observed safety-related findings.
- **Human Review:** Flag results requiring further interpretation rather than treating automated findings as definitive clinical judgements.

## How It Works

StressTheBot follows a structured evaluation pipeline:

1. **Scenario Generation:** Generate synthetic patient profiles using configurable clinical parameters.
2. **LLM Execution:** Submit scenarios to selected language models.
3. **Response Extraction:** Extract relevant information from the generated responses.
4. **Clinical Rule Evaluation:** Compare extracted response content against sourced clinical safety rules.
5. **Risk Mapping:** Organise potential violations, missing expected behaviours and other evaluation findings.
6. **Analysis and Comparison:** Present results through dashboards, risk analysis and model comparison.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript |
| UI and Visualisation | CSS, Chart.js |
| Backend | Python, FastAPI |
| Data Validation | Pydantic |
| AI Integration | LLM APIs |
| Evaluation | Python-based rule engine |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Project Structure

```text
StressTheBot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── data/
│   │   │   └── clinical_rules/
│   │   ├── evaluation/
│   │   ├── llm/
│   │   ├── rules/
│   │   ├── scenarios/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   └── package.json
│
└── README.md
```

*The structure above describes the main application areas; individual files may evolve as development continues.*

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Poorvi-M/StressTheBot.git
cd StressTheBot
```

### 2. Set up the backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows – Git Bash:**

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required API credentials and environment variables in a local `.env` file, following the backend configuration.

Start the backend:

```bash
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Set up the frontend

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Current Evaluation Limitations

StressTheBot is an evolving research prototype. Its current evaluation mechanism has important limitations:

- Automated response extraction uses pattern-based and keyword-based methods.
- Rule evaluation identifies evidence candidates through configured patterns; it does not reliably understand clinical context, negation or semantic intent.
- A potential violation or missing expected behaviour is an evaluation finding, not proof of clinical harm.
- Clinical rules are currently maintained in draft status and are intended for research-only evaluation.
- Severity classifications are provisional and require appropriate expert review.
- Automated results must not be interpreted as clinical safety certification.

Clinical rule approval and interpretation require qualified human review.

## Future Development

Planned areas of development include:

- Expanding the clinical safety rule repository with additional authoritative sources.
- Increasing the diversity and complexity of synthetic clinical scenarios.
- Improving semantic response extraction and evaluation.
- Supporting additional LLM providers.
- Developing more comprehensive parameter-sweep experiments.
- Enhancing risk visualisation and model comparison.
- Introducing clinician review and rule-validation workflows.
- Dockerising the application for containerised deployment.
- Deploying the frontend and backend for public access.

## Research Direction

The central objective of StressTheBot is to move beyond aggregate model performance and investigate **where, why and under what patient conditions clinical AI safety failures may occur**.

By combining reproducible synthetic scenarios, source-linked safety constraints, structured evaluation and scenario-level risk analysis, the platform aims to make clinical LLM evaluation more transparent and actionable.

---

**Developed as a research-oriented clinical AI safety evaluation project.**
