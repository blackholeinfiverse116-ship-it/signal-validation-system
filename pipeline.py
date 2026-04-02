from src.validation.signal_validator import validate_signal
from src.samachar_adapter import samachar_to_signal
from src.mitra.mitra_interface import get_decision


def run_pipeline(events):

    results = []

    for event in events:

        try:
            # 🔁 STEP 1: Samachar → Signal
            signal = samachar_to_signal(event)

        except Exception as e:
            results.append({
                "error": f"Samachar Adapter Error: {str(e)}"
            })
            continue

        try:
            # 🚨 STEP 2: VALIDATION
            validation = validate_signal(signal)

        except Exception as e:
            results.append({
                "error": f"Validation Error: {str(e)}"
            })
            continue

        # ❌ PIPELINE LOCK (CRITICAL)
        if validation["status"] == "REJECT":
            results.append({
                "validation": validation,
                "error": "Pipeline stopped due to REJECT"
            })
            continue

        try:
            # 🔁 STEP 3: MITRA DECISION
            decision = get_decision(validation)

        except Exception as e:
            results.append({
                "validation": validation,
                "error": "Mitra unavailable",
                "trace_id": validation.get("trace_id")
            })
            continue

        # ✅ FINAL OUTPUT (VALIDATION + DECISION)
        results.append({
            "validation": validation,
            "decision": decision
        })

    return results