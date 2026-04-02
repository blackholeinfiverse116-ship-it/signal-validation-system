import sys
import os

# 🔧 Fix import path
sys.path.append(
    os.path.abspath(os.path.dirname(__file__))
)

from src.pipeline import run_pipeline


# 🔥 SAMACHAR RAW INPUT (BATCH)
signals = [

    # ✅ VALID SIGNAL (ALLOW)
    {
        "id": 1,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 10,
        "dataset_id": "1"
    },

    # ⚠️ FLAG CASE
    {
        "id": 2,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": None,
        "dataset_id": "2"
    },

    # ❌ REJECT CASE (future timestamp)
    {
        "id": 3,
        "time": "2035-01-01 10:00:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 20,
        "dataset_id": "1"
    },

    # ❌ REJECT CASE (invalid dataset)
    {
        "id": 4,
        "time": "2025-03-25 10:30:00",
        "lat": 28.6,
        "lon": 77.2,
        "type": "movement",
        "value": 15,
        "dataset_id": "999"
    }
]


# 🚀 RUN FULL BATCH (IMPORTANT)
print("\n🚀 RUNNING END-TO-END PIPELINE DEMO...\n")

results = run_pipeline(signals)


# 🎯 PRINT RESULTS CLEANLY
for i, result in enumerate(results, start=1):

    print(f"🔹 Signal {i} Result:\n")

    # ❌ ERROR CASE
    if "error" in result:
        print(f"  ❌ Error: {result['error']}")
        if "trace_id" in result:
            print(f"  🔗 Trace ID: {result['trace_id']}")
        print("\n" + "=" * 60 + "\n")
        continue

    validation = result.get("validation", {})
    decision = result.get("decision", {})

    # ✅ VALIDATION OUTPUT
    print("  ✅ VALIDATION:")
    print(f"     Status: {validation.get('status')}")
    print(f"     Confidence: {round(validation.get('confidence_score', 0), 2)}")
    print(f"     Dataset: {validation.get('dataset_id')}")

    # ✅ DECISION OUTPUT (MITRA)
    print("\n  🧠 DECISION (MITRA):")
    print(f"     Status: {decision.get('status')}")
    print(f"     Risk Level: {decision.get('risk_level')}")
    print(f"     Reason: {decision.get('reason')}")

    # 🔗 TRACE ID (VERY IMPORTANT)
    print(f"\n  🔗 Trace ID: {validation.get('trace_id')}")

    print("\n" + "=" * 60 + "\n")