import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.pipeline import run_pipeline


events = [

    # ✅ VALID
    {
        "id": 1,
        "dataset_id": "1",
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 45
    },

    # ❌ Missing dataset_id
    {
        "id": 2,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 45
    },

    # ❌ Future timestamp
    {
        "id": 3,
        "dataset_id": "1",
        "time": "2035-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 45
    },

    # ❌ Invalid latitude
    {
        "id": 4,
        "dataset_id": "1",
        "time": "2025-03-25 10:30:00",
        "lat": 200,
        "lon": 77.2,
        "type": "movement",
        "value": 45
    },

    # ❌ Invalid value type
    {
        "id": 5,
        "dataset_id": "1",
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": "45"
    },

    # ⚠️ FLAG (null value)
    {
        "id": 6,
        "dataset_id": "1",
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": None
    }
]


print("\n--- PIPELINE RESULTS (END-TO-END) ---\n")

results = run_pipeline(events)

for i, result in enumerate(results):

    print(f"\nEvent {i+1}:")

    # ❌ ERROR CASE
    if "error" in result:
        print(f"  Error: {result['error']}")
        continue

    validation = result.get("validation", {})
    decision = result.get("decision", {})

    print(
        f"  Status: {validation.get('status')} | "
        f"Confidence: {round(validation.get('confidence_score', 0), 2)}"
    )

    print(
        f"  Decision: {decision.get('status')} | "
        f"Risk: {decision.get('risk_level')}"
    )

    print(f"  Trace ID: {validation.get('trace_id')}")