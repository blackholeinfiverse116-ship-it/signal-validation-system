from datetime import datetime
import os
import uuid
from src.validation.dataset_registry import is_valid_dataset, get_dataset_trust_score

# ---------------- CONSTANTS ----------------
ALLOWED_FEATURE_TYPES = [
    "movement",
    "communication",
    "environmental"
]


# ---------------- LOGGING ----------------
def log_rejected_signal(signal, reason):
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    logs_dir = os.path.join(base_dir, "logs")

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, "rejected_signals.log")

    with open(log_file, "a") as file:
        file.write(
            f"[REJECT] {datetime.now()} | "
            f"SignalID={signal.get('signal_id')} | "
            f"Dataset={signal.get('dataset_id')} | "
            f"Reason={reason}\n"
        )


# ---------------- STANDARD RESPONSE ----------------
def build_response(signal, status, confidence, trace_id):
    return {
        "signal_id": signal.get("signal_id"),
        "dataset_id": str(signal.get("dataset_id")),
        "status": status,
        "confidence_score": confidence,
        "validation_type": "DATA_TRUST",
        "timestamp": signal.get("timestamp"),
        "trace_id": trace_id
    }


# ---------------- CONFIDENCE ----------------
def calculate_confidence(signal, trust_score):
    score = 1.0

    if signal.get("value") is None:
        score -= 0.3

    score *= trust_score

    return max(0.0, min(score, 1.0))


# ---------------- VALIDATION ----------------
def validate_signal(signal):

    trace_id = str(uuid.uuid4())

    # 🔴 REQUIRED FIELDS
    required_fields = ["signal_id", "dataset_id", "timestamp", "feature_type"]

    for field in required_fields:
        if signal.get(field) in [None, ""]:
            log_rejected_signal(signal, f"Missing field: {field}")
            return build_response(signal, "REJECT", 0.0, trace_id)

    dataset_id = signal.get("dataset_id")
    timestamp = signal.get("timestamp")
    feature_type = signal.get("feature_type")
    value = signal.get("value")
    latitude = signal.get("latitude")
    longitude = signal.get("longitude")

    # 🔴 DATASET VALIDATION
    is_valid, dataset_info = is_valid_dataset(dataset_id)

    if not is_valid:
        log_rejected_signal(signal, str(dataset_info))
        return build_response(signal, "REJECT", 0.0, trace_id)

    trust_score = get_dataset_trust_score(dataset_id)

    # 🔴 TIMESTAMP VALIDATION
    try:
        ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        if ts > datetime.now():
            log_rejected_signal(signal, "Future timestamp")
            return build_response(signal, "REJECT", 0.0, trace_id)

    except ValueError:
        log_rejected_signal(signal, "Invalid timestamp format")
        return build_response(signal, "REJECT", 0.0, trace_id)

    # 🔴 LOCATION VALIDATION
    if latitude is None or not (-90 <= latitude <= 90):
        log_rejected_signal(signal, "Invalid latitude")
        return build_response(signal, "REJECT", 0.0, trace_id)

    if longitude is None or not (-180 <= longitude <= 180):
        log_rejected_signal(signal, "Invalid longitude")
        return build_response(signal, "REJECT", 0.0, trace_id)

    # 🔴 FEATURE TYPE VALIDATION
    if feature_type not in ALLOWED_FEATURE_TYPES:
        log_rejected_signal(signal, "Invalid feature_type")
        return build_response(signal, "REJECT", 0.0, trace_id)

    # 🔴 VALUE TYPE CHECK
    if value is not None and not isinstance(value, (int, float)):
        log_rejected_signal(signal, "Invalid value type")
        return build_response(signal, "REJECT", 0.0, trace_id)

    # 🔴 CONFIDENCE
    confidence = calculate_confidence(signal, trust_score)

    # 🟡 FLAG CONDITIONS
    if value is None:
        return build_response(signal, "FLAG", confidence, trace_id)

    if trust_score < 0.7:
        return build_response(signal, "FLAG", confidence, trace_id)

    if confidence < 0.7:
        return build_response(signal, "FLAG", confidence, trace_id)

    # 🟢 ALLOW
    return build_response(signal, "ALLOW", confidence, trace_id)