# LangGraph Invoice Processing Agent with HITL

This project implements a **LangGraph-based Invoice Processing Agent** that demonstrates:

- Graph-based orchestration
- Persistent state management
- Human-In-The-Loop (HITL) checkpoint & resume
- Dynamic tool selection (Bigtool pattern)
- Simple Human Review UI using FastAPI

The goal is to show **how complex business workflows can pause, wait for human decisions, and resume safely without reprocessing earlier steps**.

---

##  Architecture Overview
INTAKE
↓
UNDERSTAND (OCR + Parsing)
↓
MATCH (2-way matching)
↓
CHECKPOINT (if match fails)
↓
HUMAN REVIEW (ACCEPT / REJECT)
↓
RESUME WORKFLOW (no re-run)


Each step is implemented as a **LangGraph node**, with shared state passed between nodes.

---

##  Project Structure
invoice_agent/
│
├── main.py # Entry point + FastAPI UI + resume logic
├── graph.py # LangGraph workflow definition
├── state.py # Shared workflow state
├── bigtool.py # Dynamic tool selection abstraction
│
├── nodes/
│ ├── intake.py
│ ├── understand.py
│ ├── match.py
│ └── checkpoint.py
│
└── db/
└── demo.db # SQLite checkpoint store


---

##  Setup Instructions

### 1️ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows

pip install langgraph fastapi uvicorn python-multipart


## Running the Workflow
### Step 1 — Trigger Invoice Processing
python main.py


Expected output (example):

MATCH score: 0.6 → FAILED
CHECKPOINT reached — pausing workflow


This creates a HITL checkpoint in the database.

## Step 2 — Start Human Review UI
### uvicorn main:app --reload


Open in browser:

http://127.0.0.1:8000/human-review


You will see pending invoices with ACCEPT / REJECT buttons.

## Step 3 — Human Decision

Click ACCEPT → workflow resumes

Click REJECT → workflow ends

Terminal output on ACCEPT:

Resuming workflow with human decision: ACCEPT
INTAKE skipped (resume)
UNDERSTAND skipped (resume)
MATCH skipped (resume)


This proves resume without reprocessing earlier steps.

##  Key Design Concepts
## LangGraph over LangChain

Explicit workflow graph

Deterministic + conditional routing

Native checkpoint & resume semantics

## Human-In-The-Loop (HITL)

Workflow pauses on low-confidence automation

Full state persisted to DB

Human decision resumes same execution

## Bigtool Pattern

Tool selection abstracted from workflow logic

Easy to swap OCR / ERP / DB providers

## MCP-style Server Separation

COMMON → internal logic

ATLAS → external system interactions (simulated)

## What This Demonstrates

Production-style orchestration

Safe automation with human oversight

Stateful, resumable workflows

Clean separation of concerns

## Future Enhancements

Real OCR / ERP integrations

Role-based reviewer authentication

Multi-invoice concurrent processing

UI enhancements (React / dashboard)


