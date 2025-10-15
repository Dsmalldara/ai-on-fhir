#!/usr/bin/env python3

from typing import Any, Dict, List, Optional, Union
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import re
import datetime
import logging

# Import static data
from data import (
    SAMPLE_PATIENTS,
    DIAGNOSIS_KEYWORDS,
    GENDER_KEYWORDS,
    AGE_OPERATORS,
    QUERY_SUGGESTIONS,
)

# Try spaCy, fall back to regex
try:
    import spacy

    nlp = spacy.load("en_core_web_sm")
    NLP_AVAILABLE = True
except Exception:
    NLP_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI on FHIR Backend",
    version="1.0",
    description="Natural language interface for FHIR patient queries",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Models ---
class AgeFilter(BaseModel):
    op: str
    age: Optional[int] = None
    low: Optional[int] = None
    high: Optional[int] = None


class ParsedFilters(BaseModel):
    raw_text: str
    age: Optional[AgeFilter] = None
    diagnoses: List[str] = Field(default_factory=list)
    gender: Optional[str] = None
    confidence: float = 1.0


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)


class HealthResponse(BaseModel):
    status: str
    nlp_available: bool
    total_patients: int


class PatientSummary(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    primary_condition: str
    medications: str


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total_results: int
    total_pages: int


class SearchPatientsResponse(BaseModel):
    data: List[PatientSummary]
    pagination: PaginationInfo


class QuerySummary(BaseModel):
    total_patients_found: int
    confidence_score: float



class AppliedFilters(BaseModel):
    age_filter: Optional[str] = None
    gender_filter: Optional[str] = None
    diagnosis_filter: Optional[List[str]] = None


class QueryResponse(BaseModel):
    parsed_filters: ParsedFilters
    applied_filters: AppliedFilters
    summary: QuerySummary
    results_sample: List[Dict[str, Any]]


class SuggestionResponse(BaseModel):
    suggestions: List[str]


class AgeDistribution(BaseModel):
    age_group: str
    count: int


class GenderDistribution(BaseModel):
    gender: str
    count: int


class ConditionDistribution(BaseModel):
    condition: str
    count: int


class ChartDataResponse(BaseModel):
    age_distribution: List[AgeDistribution]
    gender_distribution: List[GenderDistribution]
    condition_distribution: List[ConditionDistribution]
    total_patients: int


class FilterOption(BaseModel):
    label: str
    value: str


class FilterOptionsResponse(BaseModel):
    age_ranges: List[FilterOption]
    genders: List[FilterOption]
    diagnoses: List[FilterOption]


# --- Utilities ---
def calculate_age(
    birth_date: str, reference_date: Optional[datetime.date] = None
) -> int:
    """Calculate age from birth date relative to reference_date (defaults to today)."""
    bd = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
    if reference_date is None:
        reference_date = datetime.date.today()
    return (
        reference_date.year
        - bd.year
        - ((reference_date.month, reference_date.day) < (bd.month, bd.day))
    )


def is_diabetes_query(text_lower: str) -> bool:
    """Detect whether the query is specifically about diabetes (various synonyms)."""
    diabetes_terms = [
        "diabetes",
        "diabetic",
        "type 1 diabetes",
        "type i diabetes",
        "t1dm",
        "type 2 diabetes",
        "type ii diabetes",
        "t2dm",
        "diabetes mellitus",
    ]
    return any(term in text_lower for term in diabetes_terms)


def get_diabetes_codes() -> List[str]:
    """Return canonical diabetes ICD codes from DIAGNOSIS_KEYWORDS if present."""
    codes = set()
    for k, v in DIAGNOSIS_KEYWORDS.items():
        if "diabetes" in k or k in (
            "t1dm",
            "t2dm",
            "type 1 diabetes",
            "type i diabetes",
            "type 2 diabetes",
            "type ii diabetes",
            "diabetes mellitus",
            "diabetic",
        ):
            codes.update(v)
    # safe fallback: common diabetes codes
    if not codes:
        codes.update(["E10", "E11"])
    return sorted(codes)


def parse_query(query: str) -> ParsedFilters:
    """Parse natural language query using spaCy or regex fallback"""
    text_lower = query.lower()
    result = {
        "raw_text": query,
        "age": None,
        "diagnoses": [],
        "gender": None,
        "confidence": 1.0,
    }

    # Gender detection
    for keyword, gender in GENDER_KEYWORDS.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
            result["gender"] = gender
            break

    # Diagnosis detection (with diabetes prioritization to avoid overbroad matches)
    diagnosed = set()
    if is_diabetes_query(text_lower):
        # If query explicitly references diabetes, restrict to diabetes codes only.
        diagnosed.update(get_diabetes_codes())
    else:
        # Normal matching across DIAGNOSIS_KEYWORDS
        for keyword, codes in DIAGNOSIS_KEYWORDS.items():
            if keyword in text_lower:
                diagnosed.update(codes)

    result["diagnoses"] = sorted(list(diagnosed))

    # Age detection - between X and Y
    between = re.search(r"between\s+(\d{1,3})\s+(?:and|to)\s+(\d{1,3})", text_lower)
    if between:
        low, high = int(between.group(1)), int(between.group(2))
        result["age"] = {"op": "between", "low": min(low, high), "high": max(low, high)}
    else:
        # Age with operator
        for phrase, op in AGE_OPERATORS.items():
            match = re.search(rf"{re.escape(phrase)}\s+(\d{{1,3}})", text_lower)
            if match:
                # op is something like '>' or '<=' from AGE_OPERATORS
                result["age"] = {"op": op, "age": int(match.group(1))}
                break

        # Age with + or patterns
        if not result["age"]:
            for pattern in [r"(\d{1,3})\+", r"age[d]?\s+(\d{1,3})"]:
                match = re.search(pattern, text_lower)
                if match:
                    result["age"] = {"op": ">=", "age": int(match.group(1))}
                    break

    # Calculate confidence (simple heuristic)
    found = sum(
        [bool(result["age"]), bool(result["diagnoses"]), bool(result["gender"])]
    )
    result["confidence"] = min(1.0, 0.4 + (found * 0.2))

    logger.info(f"Parsed: {result}")
    return ParsedFilters(**result)


def _validate_system_date_against_data(
    reference_date: datetime.date, patients: List[Dict]
) -> bool:
    """
    Ensure system reference_date is sensible relative to patient birth dates.
    Returns True if date is OK; False if there is at least one birthDate in the future
    compared to reference_date (indicates clock problem or bad data).
    """
    for p in patients:
        try:
            bd = datetime.datetime.strptime(p["birthDate"], "%Y-%m-%d").date()
            if bd > reference_date:
                logger.warning(
                    f"Patient {p.get('id')} has birthDate {bd} which is after reference date {reference_date}. Skipping age-based filtering."
                )
                return False
        except Exception as exc:
            logger.exception(f"Bad birthDate for patient {p.get('id')}: {exc}")
            return False
    return True


def _apply_age_filter(patients: List[Dict], age_filter: str, today: datetime.date) -> List[Dict]:
    """Apply age filter logic to patient list."""
    # Range like "30-50"
    if "-" in age_filter and age_filter.count("-") == 1 and age_filter.split("-")[0].isdigit():
        low_s, high_s = age_filter.split("-")
        low, high = int(low_s), int(high_s)
        return [
            p for p in patients
            if low <= calculate_age(p["birthDate"], reference_date=today) <= high
        ]
    
    # Operator-prefixed filters: e.g. ">60", ">=60", "<=70", "<50"
    m = re.match(r"^(>=|<=|>|<)?\s*(\d{1,3})\+?$", age_filter.strip())
    if m:
        op = m.group(1) or ">="
        age_val = int(m.group(2))
        ops = {
            ">": lambda age: age > age_val,
            ">=": lambda age: age >= age_val,
            "<": lambda age: age < age_val,
            "<=": lambda age: age <= age_val,
        }
        return [
            p for p in patients
            if ops[op](calculate_age(p["birthDate"], reference_date=today))
        ]
    
    # Fallback: "60+" or exact age "60"
    if age_filter.endswith("+") and age_filter[:-1].isdigit():
        min_age = int(age_filter[:-1])
        return [
            p for p in patients
            if calculate_age(p["birthDate"], reference_date=today) >= min_age
        ]
    elif age_filter.isdigit():
        age_val = int(age_filter)
        return [
            p for p in patients
            if calculate_age(p["birthDate"], reference_date=today) == age_val
        ]
    
    return patients


def filter_patients(
    age_filter: Optional[str] = None,
    gender_filter: Optional[str] = None,
    diagnosis_filter: Optional[Union[str, List[str]]] = None,
) -> List[Dict]:
    """Apply filters to patient dataset."""
    patients = SAMPLE_PATIENTS.copy()

    # Gender filter
    if gender_filter:
        patients = [p for p in patients if p.get("gender") == gender_filter]

    # Diagnosis filter (support list)
    if diagnosis_filter:
        diag_codes = {diagnosis_filter} if isinstance(diagnosis_filter, str) else set(diagnosis_filter)
        patients = [
            p for p in patients
            if any(c.get("code") in diag_codes for c in p.get("conditions", []))
        ]

    # Age filter
    if age_filter:
        today = datetime.date.today()
        if not _validate_system_date_against_data(today, patients):
            logger.error("System date out-of-sync with patient birth dates. Age filter skipped.")
            return patients
        
        patients = _apply_age_filter(patients, age_filter, today)

    return patients


# --- API Endpoints ---
@app.get("/health", response_model=HealthResponse)
def health():
    """Health check"""
    return {
        "status": "ok",
        "nlp_available": NLP_AVAILABLE,
        "total_patients": len(SAMPLE_PATIENTS),
    }


@app.post("/query", response_model=QueryResponse)
def query_endpoint(body: QueryRequest):
    """Parse natural language query and return parsed filters + summary"""
    filters = parse_query(body.query)

    # Convert to filter parameters (keep operator semantics explicit)
    applied = {}
    if filters.age:
        if filters.age.op == "between":
            applied["age_filter"] = f"{filters.age.low}-{filters.age.high}"
        elif filters.age.age is not None:
            # preserve operator; use explicit prefixes so filter_patients can interpret correctly
            if filters.age.op in (">", ">="):
                applied["age_filter"] = f"{filters.age.op}{filters.age.age}"
            elif filters.age.op in ("<", "<="):
                applied["age_filter"] = f"{filters.age.op}{filters.age.age}"
            else:
                # fallback: default to >= for patterns like "50+"
                applied["age_filter"] = f">={filters.age.age}"

    if filters.gender:
        applied["gender_filter"] = filters.gender

    if filters.diagnoses:
        # pass the full diagnosis list (not just the first) to avoid dropping potential matches
        applied["diagnosis_filter"] = filters.diagnoses

    # Count matches
    try:
        matching = filter_patients(
            age_filter=applied.get("age_filter"),
            gender_filter=applied.get("gender_filter"),
            diagnosis_filter=applied.get("diagnosis_filter"),
        )
    except Exception as exc:
        # If age validation failed or similar, return an error with explanation
        logger.exception("Error filtering patients")
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "parsed_filters": filters,
        "applied_filters": applied,
        "summary": {
            "total_patients_found": len(matching),
            "confidence_score": filters.confidence,
        },
        "results_sample": matching[:10],
    }


@app.get("/suggestions", response_model=SuggestionResponse)
def suggestions(q: str = ""):
    """Query autocomplete suggestions"""
    if not q:
        return {"suggestions": QUERY_SUGGESTIONS[:8]}

    q_lower = q.lower()
    filtered = [s for s in QUERY_SUGGESTIONS if q_lower in s.lower()]
    return {"suggestions": filtered[:10]}


@app.get("/analytics/chart-data", response_model=ChartDataResponse)
def chart_data(
    age_filter: Optional[str] = None,
    gender_filter: Optional[str] = None,
    diagnosis_filter: Optional[str] = None,
):
    """Get aggregated data for charts (no PII)"""
    patients = filter_patients(age_filter, gender_filter, diagnosis_filter)

    # Age distribution
    age_buckets = {"0-30": 0, "31-50": 0, "51-70": 0, "71+": 0}
    for p in patients:
        age = calculate_age(p["birthDate"])
        if age <= 30:
            age_buckets["0-30"] += 1
        elif age <= 50:
            age_buckets["31-50"] += 1
        elif age <= 70:
            age_buckets["51-70"] += 1
        else:
            age_buckets["71+"] += 1

    # Gender distribution
    gender_dist = {"male": 0, "female": 0}
    for p in patients:
        gender_dist[p["gender"]] += 1

    # Condition distribution
    condition_counts = {}
    for p in patients:
        for c in p["conditions"]:
            condition_counts[c["display"]] = condition_counts.get(c["display"], 0) + 1

    return {
        "age_distribution": [
            {"age_group": k, "count": v} for k, v in age_buckets.items()
        ],
        "gender_distribution": [
            {"gender": k.capitalize(), "count": v} for k, v in gender_dist.items()
        ],
        "condition_distribution": [
            {"condition": k, "count": v}
            for k, v in sorted(condition_counts.items(), key=lambda x: -x[1])
        ],
        "total_patients": len(patients),
    }


@app.get("/patients/search", response_model=SearchPatientsResponse)
def search_patients(
    age_filter: Optional[str] = None,
    gender_filter: Optional[str] = None,
    diagnosis_filter: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
):
    """Search patients with pagination (for table display)"""
    patients = filter_patients(age_filter, gender_filter, diagnosis_filter)

    # Format for table
    table_data = []
    for p in patients:
        table_data.append(
            {
                "id": p["id"],
                "name": f"{p['name']['given'][0]} {p['name']['family']}",
                "age": calculate_age(p["birthDate"]),
                "gender": p["gender"].capitalize(),
                "primary_condition": (
                    p["conditions"][0]["display"] if p["conditions"] else "None"
                ),
                "medications": ", ".join(p.get("medications", [])),
            }
        )

    # Pagination
    total = len(table_data)
    start = (page - 1) * limit
    end = start + limit
    paginated = table_data[start:end]

    return {
        "data": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_results": total,
            "total_pages": (total + limit - 1) // limit,
        },
    }


@app.get("/filters/options", response_model=FilterOptionsResponse)
def filter_options():
    """Get available filter options for dropdowns"""
    all_conditions = {}
    for p in SAMPLE_PATIENTS:
        for c in p["conditions"]:
            all_conditions[c["code"]] = c["display"]

    return {
        "age_ranges": [
            {"label": "Under 30", "value": "<30"},
            {"label": "30-50", "value": "30-50"},
            {"label": "50-70", "value": "50-70"},
            {"label": "70+", "value": "70+"},
        ],
        "genders": [
            {"label": "Male", "value": "male"},
            {"label": "Female", "value": "female"},
        ],
        "diagnoses": [
            {"label": display, "value": code}
            for code, display in sorted(all_conditions.items(), key=lambda x: x[1])
        ],
    }


if __name__ == "__main__":
    print("AI on FHIR Backend - Streamlined Version (updated)")
    print("=" * 60)
    print("To run: uvicorn main:app --reload --port 8000")
    print("API docs: http://localhost:8000/docs")
    print("=" * 60)