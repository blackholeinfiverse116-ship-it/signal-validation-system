# 🔷 Trust Enforcement & Validation System

---

## 📌 Project Overview

This project implements a **fully integrated trust enforcement pipeline** that ensures only validated and governed signals enter the system.

It acts as a **system-level gatekeeper** before downstream layers like:

* Mitra (Decision Layer)
* CET (Post-validation logic)
* Simulation (Rudra / Atharva)
* UI (Frontend Integration)

---

## 🎯 Objective

To build a **non-bypassable, traceable, and integration-ready system** that:

* Prevents invalid data entry
* Flags suspicious signals
* Enforces strict validation rules
* Maintains trace continuity across layers
* Supports real system flow (not isolated validation)

---

## ⚙️ System Flow

```
Samachar (Raw Input)
        ↓
Adapter (samachar_to_signal)
        ↓
Validation Layer (signal_validator)
        ↓
Pipeline (Validation + Mitra + Enforcement)
        ↓
Mitra (Decision Layer)
        ↓
API Response (UI Ready Output)
```

---

## 🚦 System Decisions

### 🔹 Validation Layer

| Status | Meaning               |
| ------ | --------------------- |
| ALLOW  | Fully valid signal    |
| FLAG   | Suspicious but usable |
| REJECT | Invalid → blocked     |

---

### 🔹 Mitra (Decision Layer)

| Status | Risk Level | Meaning        |
| ------ | ---------- | -------------- |
| ALLOW  | LOW        | Trusted signal |
| FLAG   | MEDIUM     | Needs review   |

---

## 📊 Key Features

* ✅ End-to-End Pipeline Integration
* ✅ Dataset Registry Enforcement
* ✅ Confidence Scoring System
* ✅ 3-State Validation (ALLOW / FLAG / REJECT)
* ✅ Strict Pipeline Lock (No Validation → No Forward)
* ✅ UUID-based Traceability (`trace_id`)
* ✅ Mitra Decision Integration
* ✅ Batch Processing Support
* ✅ Structured API Output (Validation + Decision)
* ✅ Rejected Signal Logging
* ✅ FastAPI-based API

---

## 🔌 API Endpoint

### ▶️ POST `/validate`

---

### ✔ Input

Supports:

* Single raw Samachar event
* Multiple events (batch input)

---

### ✔ Output

```json
{
  "results": [
    {
      "validation": {
        "signal_id": 1,
        "dataset_id": "1",
        "status": "ALLOW",
        "confidence_score": 0.9,
        "validation_type": "DATA_TRUST",
        "timestamp": "2025-03-25 10:30:00",
        "trace_id": "uuid"
      },
      "decision": {
        "status": "ALLOW",
        "risk_level": "LOW",
        "reason": "Signal validated and trusted"
      }
    }
  ]
}
```

---

### ❌ Error Handling

* REJECT → HTTP 400
* All signals rejected → HTTP 400
* Invalid input → HTTP 400

✔ Clean and structured error responses

---

## 🧪 Test Cases

| Case                | Expected Result |
| ------------------- | --------------- |
| Missing dataset_id  | REJECT          |
| Invalid dataset     | REJECT          |
| Inactive dataset    | REJECT          |
| Future timestamp    | REJECT          |
| Invalid coordinates | REJECT          |
| Invalid data type   | REJECT          |
| Null value          | FLAG            |
| Low trust dataset   | FLAG            |
| Valid signal        | ALLOW           |
| Mixed batch         | Partial success |

---

## 📁 Project Structure

```
src/
 ├── validation/
 │    ├── signal_validator.py
 │    ├── dataset_registry.py
 │
 ├── samachar_adapter.py
 ├── pipeline.py
 │
 ├── mitra/
 │    ├── mitra_interface.py
 │
 ├── api/
 │    ├── main.py

logs/
 ├── rejected_signals.log

run_demo_validation.py
REVIEW_PACKET.md
README.md
```

---

## ▶️ How to Run

### 🔹 1. Install Dependencies

```
pip install fastapi uvicorn
```

---

### 🔹 2. Run Demo (Without API)

```
python run_demo_validation.py
```

---

### 🔹 3. Run API

```
python -m uvicorn src.api.main:app --reload
```

---

### 🔹 4. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🧪 API Testing Examples

---

### ✅ 1. Valid Signal (ALLOW)

```json
{
  "id": 1,
  "time": "2025-03-25 10:30:00",
  "lat": 28.6,
  "lon": 77.2,
  "type": "movement",
  "value": 10,
  "dataset_id": "1"
}
```

---

### ⚠️ 2. FLAG Signal

```json
{
  "id": 2,
  "time": "2025-03-25 10:30:00",
  "lat": 28.6,
  "lon": 77.2,
  "type": "movement",
  "value": null,
  "dataset_id": "2"
}
```

---

### ❌ 3. REJECT Signal

```json
{
  "id": 3,
  "time": "2035-01-01 10:00:00",
  "lat": 28.6,
  "lon": 77.2,
  "type": "movement",
  "value": 20,
  "dataset_id": "1"
}
```

---

### 🔁 4. Batch Input

```json
[
  { "id": 1, "time": "...", "lat": 28.6, "lon": 77.2, "type": "movement", "value": 10, "dataset_id": "1" },
  { "id": 2, "time": "...", "lat": 28.6, "lon": 77.2, "type": "movement", "value": null, "dataset_id": "2" }
]
```

---

## 🧾 Logging

Rejected signals are stored in:

```
logs/rejected_signals.log
```

Each log includes:

* timestamp
* signal_id
* dataset_id
* reason

✔ Enables debugging
✔ Ensures audit trail

---

## 🔐 System Guarantees

* ✔ No invalid data enters system
* ✔ Validation is mandatory
* ✔ REJECT stops pipeline
* ✔ FLAG signals are safely processed
* ✔ Deterministic outputs
* ✔ Full traceability via `trace_id`
* ✔ End-to-end control enforced

---

## 🔗 Integration Readiness

Fully compatible with:

* Samachar (Input Layer)
* Mitra (Decision Layer)
* CET (Validation Extension Layer)
* Simulation (Rudra / Atharva)
* UI (Frontend Integration)

---

## 🚀 Final Outcome

This system implements a:

👉 **Fully Integrated Trust Enforcement Pipeline**

Ensuring:

* Data integrity
* Controlled processing
* Safe downstream flow
* Decision-aware outputs
* Traceable system behavior

---

## 🏁 Conclusion

The project evolves from basic validation into a:

👉 **Production-Ready, End-to-End Trust Boundary System**

Guaranteeing:

> ❝ No untrusted signal can enter the system ❞

✔ Fully compliant
✔ Fully integrated
✔ Fully traceable
✔ Ready for real-world deployment

---
