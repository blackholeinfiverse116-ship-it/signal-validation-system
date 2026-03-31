# 🔷 Signal Validation & Trust Enforcement System

---

## 📌 Project Overview

This project implements a **strict trust enforcement layer** that ensures only validated and trusted signals enter the system.

It acts as a **gatekeeper before downstream systems** like Mitra, CET, Simulation, and UI.

---

## 🎯 Objective

To build a **non-bypassable validation system** that:

* Prevents invalid data entry
* Flags suspicious data
* Ensures trusted signal flow
* Maintains full traceability using `trace_id`

---

## ⚙️ System Flow

```
Samachar (Raw Input)
        ↓
Adapter (samachar_to_signal)
        ↓
Validation Layer (signal_validator)
        ↓
Pipeline Enforcement (pipeline.py)
        ↓
Mitra (Decision Layer)
        ↓
API Output (UI Ready)
```

---

## 🚦 Validation Decisions

| Status | Description           |
| ------ | --------------------- |
| ALLOW  | Valid signal          |
| FLAG   | Suspicious but usable |
| REJECT | Invalid (blocked)     |

---

## 📊 Features

* ✅ Dataset Registry Enforcement
* ✅ Confidence Scoring System
* ✅ FLAG Logic (not just binary)
* ✅ Strict Pipeline Lock (No Validation → No Forward)
* ✅ UUID-based Traceability (`trace_id`)
* ✅ Structured API Output
* ✅ Logging of Rejected Signals
* ✅ FastAPI Integration Ready

---

## 🔌 API Endpoint

### POST `/validate`

### ✔ Input:

Raw Samachar event

### ✔ Output:

Standardized validation response:

```json
{
  "signal_id": 1,
  "dataset_id": "1",
  "status": "ALLOW",
  "confidence_score": 0.9,
  "validation_type": "DATA_TRUST",
  "timestamp": "2025-03-25 10:30:00",
  "trace_id": "uuid"
}
```

### ✔ Error Handling:

* REJECT → HTTP 400
* Invalid input → HTTP 400

---

## 🧪 Test Cases

| Case               | Expected Result |
| ------------------ | --------------- |
| Missing dataset_id | REJECT          |
| Invalid dataset    | REJECT          |
| Inactive dataset   | REJECT          |
| Future timestamp   | REJECT          |
| Null value         | FLAG            |
| Low confidence     | FLAG            |
| Valid signal       | ALLOW           |

---

## 📁 Project Structure

```
src/
 ├── validation/
 │    ├── signal_validator.py
 │    ├── dataset_registry.py
 │
 ├── pipeline.py
 ├── samachar_adapter.py
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

### 🔹 1. Install dependencies

```
pip install fastapi uvicorn
```

### 🔹2.Run Demo Script (Without API)

This runs sample test cases directly through the pipeline.

python run_demo_validation.py

### 🔹 3. Run API

```
python -m uvicorn src.api.main:app --reload
```

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

### ⚠️ 2. Suspicious Signal (FLAG)

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

### ❌ 3. Invalid Signal (REJECT)

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

## 🧾 Logging

Rejected signals are stored in:

```
logs/rejected_signals.log
```

Each log contains:

* timestamp
* signal_id
* dataset_id
* reason

✔ Ensures full traceability

---

## 🔐 System Guarantees

* ✔ No invalid data enters the system
* ✔ Validation is mandatory (no bypass possible)
* ✔ REJECT immediately stops pipeline
* ✔ FLAG signals are safely forwarded
* ✔ Deterministic behavior
* ✔ Full traceability using `trace_id`

---

## 🔗 Integration Readiness

This system is fully compatible with:

* Samachar (Input Layer)
* Mitra (Decision Layer)
* CET (Post-validation logic)
* Simulation (Rudra / Atharva)
* UI (Nikhil)

---

## 🚀 Final Outcome

This project transforms a basic validator into a:

👉 **Production-Ready Trust Enforcement Layer**

Ensuring:

* Data integrity
* Reliable processing
* Safe downstream integration
* End-to-end traceability

---

## 🏁 Conclusion

The system establishes a **strict trust boundary** that guarantees:

> ❝ No untrusted signal can enter the system ❞

Making it ready for real-world, large-scale distributed systems.
