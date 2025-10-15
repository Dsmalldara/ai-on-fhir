# AI on FHIR – Streamlined Backend

A lightweight **FastAPI backend** that interprets natural-language healthcare queries and converts them into **FHIR-style search requests** over static sample data.

This implementation covers **Part 1 of the AI on FHIR assessment (Backend & NLP Integration)**. It is **containerized with Docker** and exposes REST endpoints for query parsing, patient search, and analytics.

---

## Overview

The service accepts queries such as:

> “Show me all diabetic patients over 60”

It then:

- Extracts structured filters (age, gender, diagnosis) using **rule-based NLP** (spaCy if available, regex fallback).  
- Converts filters into a simulated **FHIR search** over synthetic patient data.  
- Returns a **mock FHIR-compliant response** and summary statistics.

---

## Key Features

- **FastAPI** with OpenAPI documentation (`/docs`)  
- **spaCy** for Natural Language Processing and regex-based NLP parser for fallback  
- **Static synthetic dataset** (no PHI)  
- **Age operator handling** (`>`, `<`, `between`)  
- **System date validation** before age filtering  
- Targeted **diabetes code isolation** (`E10`, `E11` only)  
- **Chart and table data endpoints** for front-end use  

---

## Prerequisites

- Docker and Docker Compose  
- (Optional) Python 3.9+ if running locally without Docker  

---

## Running with Docker

1. **Build the image**

```bash
docker build -t ai-on-fhir-backend .
Run the container

bash
Copy code
docker run -d -p 8000:8000 ai-on-fhir-backend
Access the API

Health check: http://localhost:8000/health

Interactive docs: http://localhost:8000/docs

Alternative Redoc: http://localhost:8000/redoc

API Endpoints
Full API specification and interactive documentation are available at /docs.

Endpoint	Method	Purpose
/health	GET	Service status and metadata
/query	POST	Parse natural-language queries and return filters/results
/patients/search	GET	Search patients with explicit filters (supports pagination)
/analytics/chart-data	GET	Aggregated data for chart visualization (no PII)
/filters/options	GET	Static dropdown filter options
/suggestions	GET	Autocomplete query suggestions

Environment Variables
Variable	Description	Default
PORT	Port exposed by FastAPI	8000
LOG_LEVEL	Logging verbosity	info

Development (Run locally without Docker)
bash
Copy code
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # or: pip install fastapi uvicorn pydantic spacy
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
Open http://localhost:8000/docs

Project Layout
bash
Copy code
.
├── main.py            # FastAPI application
├── data.py            # Static sample patients and keyword mappings
├── Dockerfile         # Container build instructions
├── docker-compose.yml
├── requirements.txt   # Python dependencies
├── examples.md        # Usage examples and sample requests for interacting with the backend API
└── README.md          # Project documentation

Notes for Reviewers
The /docs endpoint contains the full OpenAPI contract and example payloads; consult it for endpoint schemas and sample responses.

This backend demonstrates NLP → simulated FHIR flow, filter semantics, and defensive checks (date validation, diagnosis isolation).

It is intentionally focused on the assessment scope and uses synthetic data only.

