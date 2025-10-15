"""
Static data module for AI on FHIR Backend
Contains sample patients and keyword mappings
"""

# Sample patient data with diverse conditions
SAMPLE_PATIENTS = [
    {
        "id": "patient-001",
        "name": {"given": ["Alice"], "family": "Smith"},
        "gender": "female",
        "birthDate": "1965-04-12",
        "conditions": [
            {"code": "E11", "display": "Type 2 diabetes mellitus"},
            {"code": "E78.5", "display": "Hyperlipidemia"},
        ],
        "medications": ["Metformin", "Atorvastatin"],
    },
    {
        "id": "patient-002",
        "name": {"given": ["Bob"], "family": "Johnson"},
        "gender": "male",
        "birthDate": "1975-11-02",
        "conditions": [{"code": "I10", "display": "Essential hypertension"}],
        "medications": ["Lisinopril"],
    },
    {
        "id": "patient-003",
        "name": {"given": ["Carol"], "family": "Nguyen"},
        "gender": "female",
        "birthDate": "1958-06-25",
        "conditions": [
            {"code": "E11", "display": "Type 2 diabetes mellitus"},
            {"code": "I10", "display": "Essential hypertension"},
        ],
        "medications": ["Metformin", "Amlodipine"],
    },
    {
        "id": "patient-004",
        "name": {"given": ["David"], "family": "Lee"},
        "gender": "male",
        "birthDate": "1988-02-14",
        "conditions": [{"code": "J45", "display": "Asthma"}],
        "medications": ["Albuterol"],
    },
    {
        "id": "patient-005",
        "name": {"given": ["Eve"], "family": "Martinez"},
        "gender": "female",
        "birthDate": "1948-01-12",
        "conditions": [
            {"code": "E10", "display": "Type 1 diabetes mellitus"},
            {"code": "I50", "display": "Heart failure"},
        ],
        "medications": ["Insulin", "Furosemide"],
    },
    {
        "id": "patient-006",
        "name": {"given": ["Frank"], "family": "Chen"},
        "gender": "male",
        "birthDate": "1992-08-30",
        "conditions": [{"code": "F41.1", "display": "Generalized anxiety disorder"}],
        "medications": ["Sertraline"],
    },
    {
        "id": "patient-007",
        "name": {"given": ["Grace"], "family": "Williams"},
        "gender": "female",
        "birthDate": "1970-03-15",
        "conditions": [
            {"code": "E11", "display": "Type 2 diabetes mellitus"},
            {"code": "M81", "display": "Osteoporosis"},
        ],
        "medications": ["Metformin", "Alendronate"],
    },
    {
        "id": "patient-008",
        "name": {"given": ["Henry"], "family": "Kumar"},
        "gender": "male",
        "birthDate": "1982-09-20",
        "conditions": [
            {"code": "J44", "display": "COPD (Chronic obstructive pulmonary disease)"},
            {"code": "I10", "display": "Essential hypertension"},
        ],
        "medications": ["Tiotropium", "Losartan"],
    },
    {
        "id": "patient-009",
        "name": {"given": ["Isabel"], "family": "Rodriguez"},
        "gender": "female",
        "birthDate": "1955-12-08",
        "conditions": [
            {"code": "I25", "display": "Chronic ischemic heart disease"},
            {"code": "E78.5", "display": "Hyperlipidemia"},
        ],
        "medications": ["Aspirin", "Metoprolol", "Rosuvastatin"],
    },
    {
        "id": "patient-010",
        "name": {"given": ["Jack"], "family": "Thompson"},
        "gender": "male",
        "birthDate": "1968-05-17",
        "conditions": [{"code": "N18", "display": "Chronic kidney disease"}],
        "medications": ["Erythropoietin", "Calcium carbonate"],
    },
    {
        "id": "patient-011",
        "name": {"given": ["Karen"], "family": "White"},
        "gender": "female",
        "birthDate": "1978-11-23",
        "conditions": [
            {"code": "M05", "display": "Rheumatoid arthritis"},
            {"code": "F41.1", "display": "Generalized anxiety disorder"},
        ],
        "medications": ["Methotrexate", "Prednisone", "Escitalopram"],
    },
    {
        "id": "patient-012",
        "name": {"given": ["Leonard"], "family": "Brown"},
        "gender": "male",
        "birthDate": "1945-03-30",
        "conditions": [
            {"code": "G30", "display": "Alzheimer's disease"},
            {"code": "I10", "display": "Essential hypertension"},
        ],
        "medications": ["Donepezil", "Amlodipine"],
    },
    {
        "id": "patient-013",
        "name": {"given": ["Maria"], "family": "Garcia"},
        "gender": "female",
        "birthDate": "1990-07-14",
        "conditions": [
            {"code": "K21", "display": "Gastroesophageal reflux disease (GERD)"}
        ],
        "medications": ["Omeprazole"],
    },
    {
        "id": "patient-014",
        "name": {"given": ["Nathan"], "family": "Park"},
        "gender": "male",
        "birthDate": "1963-01-25",
        "conditions": [
            {"code": "C50", "display": "Breast cancer (male)"},
            {"code": "F33", "display": "Major depressive disorder"},
        ],
        "medications": ["Tamoxifen", "Sertraline"],
    },
    {
        "id": "patient-015",
        "name": {"given": ["Olivia"], "family": "Anderson"},
        "gender": "female",
        "birthDate": "1985-06-09",
        "conditions": [
            {"code": "E03", "display": "Hypothyroidism"},
            {"code": "D50", "display": "Iron deficiency anemia"},
        ],
        "medications": ["Levothyroxine", "Ferrous sulfate"],
    },
]


# Diagnosis keyword mappings for NLP parsing
DIAGNOSIS_KEYWORDS = {
    # Diabetes
    "type 2 diabetes": ["E11"],
    "type ii diabetes": ["E11"],
    "t2dm": ["E11"],
    "type 1 diabetes": ["E10"],
    "type i diabetes": ["E10"],
    "t1dm": ["E10"],
    "diabetes mellitus": ["E11", "E10"],
    "diabetic": ["E11", "E10"],
    "diabetes": ["E11", "E10"],
    # Cardiovascular
    "hypertension": ["I10"],
    "high blood pressure": ["I10"],
    "htn": ["I10"],
    "heart failure": ["I50"],
    "chf": ["I50"],
    "congestive heart failure": ["I50"],
    "hyperlipidemia": ["E78.5"],
    "high cholesterol": ["E78.5"],
    "ischemic heart disease": ["I25"],
    "coronary artery disease": ["I25"],
    "cad": ["I25"],
    "ihd": ["I25"],
    # Respiratory
    "asthma": ["J45"],
    "copd": ["J44"],
    "chronic obstructive pulmonary disease": ["J44"],
    # Mental health
    "anxiety": ["F41.1"],
    "generalized anxiety disorder": ["F41.1"],
    "gad": ["F41.1"],
    "depression": ["F33"],
    "major depressive disorder": ["F33"],
    "mdd": ["F33"],
    # Musculoskeletal
    "osteoporosis": ["M81"],
    "rheumatoid arthritis": ["M05"],
    "ra": ["M05"],
    "arthritis": ["M05"],
    # Neurological
    "alzheimer": ["G30"],
    "alzheimer's disease": ["G30"],
    "dementia": ["G30"],
    # Renal
    "kidney disease": ["N18"],
    "chronic kidney disease": ["N18"],
    "ckd": ["N18"],
    # Gastrointestinal
    "gerd": ["K21"],
    "acid reflux": ["K21"],
    "gastroesophageal reflux": ["K21"],
    # Oncology
    "cancer": ["C50"],
    "breast cancer": ["C50"],
    # Endocrine
    "hypothyroidism": ["E03"],
    "thyroid": ["E03"],
    # Hematology
    "anemia": ["D50"],
    "iron deficiency": ["D50"],
}


# Gender keyword mappings
GENDER_KEYWORDS = {
    "male": "male",
    "man": "male",
    "men": "male",
    "m": "male",
    "female": "female",
    "woman": "female",
    "women": "female",
    "f": "female",
}


# Age operator mappings
AGE_OPERATORS = {
    "over": ">",
    "older than": ">",
    "greater than": ">",
    "above": ">",
    "at least": ">=",
    "under": "<",
    "younger than": "<",
    "less than": "<",
    "below": "<",
}


# Query suggestions for autocomplete
QUERY_SUGGESTIONS = [
    "Show me all diabetic patients over 50",
    "List female patients older than 60 with hypertension",
    "Patients between 40 and 70 with asthma",
    "Male patients under 35",
    "Patients aged 75+ with diabetes",
    "Women with heart failure",
    "Patients with COPD over 60",
    "Female patients with rheumatoid arthritis",
    "Patients with anxiety under 40",
    "Patients with Alzheimer's disease over 70",
    "Male patients with kidney disease",
    "Patients with GERD",
    "Female patients with thyroid disease",
]
