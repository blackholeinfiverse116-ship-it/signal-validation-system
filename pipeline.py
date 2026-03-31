from src.validation.signal_validator import validate_signal
from src.samachar_adapter import samachar_to_signal


def run_pipeline(events):

    results = []

    for event in events:

        # 🔁 STEP 1: Samachar → Signal
        signal = samachar_to_signal(event)

        # 🚨 STEP 2: VALIDATION
        validation = validate_signal(signal)

        # ❌ DO NOT raise exception here
        # Just append result
        results.append(validation)

    return results