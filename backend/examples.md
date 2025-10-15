## Example Queries

### 1️⃣ How many diabetic patients are over 50?

**Request**

```http
POST /query
Content-Type: application/json

{
  "query": "how many diabetic patients are over 50"
}


Response (simplified)

{
  "parsed_filters": {
    "raw_text": "how many  diabetic patients are  over 50",
    "age": {
      "op": ">",
      "age": 50,
      "low": null,
      "high": null
    },
    "diagnoses": [
      "E10",
      "E11"
    ],
    "gender": null,
    "confidence": 0.8
  },
  "applied_filters": {
    "age_filter": ">50",
    "diagnosis_filter": [
      "E10",
      "E11"
    ]
  },
  "summary": {
    "total_patients_found": 4,
    "confidence_score": 0.8
  },
}



### 2️⃣ Show me all kidney disease patients
 {
 "query" :"Show me all kidney disease patients"}


Response (simplified)

{
  "parsed_filters": {
    "raw_text": "Show me all kidney disease patients ",
    "age": null,
    "diagnoses": [
      "N18"
    ],
    "gender": null,
    "confidence": 0.6000000000000001
  },
  "applied_filters": {
    "diagnosis_filter": [
      "N18"
    ]
  },
  "summary": {
    "total_patients_found": 1,
    "confidence_score": 0.6000000000000001
  },
}


### 3️⃣ Show me all hypertension patients

 {
    "query" : "Show me all hypertension  patients"
}


    Response (simplified)
    {
  "parsed_filters": {
    "raw_text": "Show me all hypertension  patients  ",
    "age": null,
    "diagnoses": [
      "I10"
    ],
    "gender": null,
    "confidence": 0.6000000000000001
  },
  "applied_filters": {
    "diagnosis_filter": [
      "I10"
    ]
  },
  "summary": {
    "total_patients_found": 4,
    "confidence_score": 0.6000000000000001
  },
    }