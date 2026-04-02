from datetime import datetime
import uuid

ALLOWED_FEATURE_TYPES = [
    "movement",
    "communication",
    "environmental"
]


def samachar_to_signal(event):

    # 🚨 REQUIRED FIELDS CHECK
    required_fields = ["id", "time", "lat", "lon", "type", "dataset_id"]

    for field in required_fields:
        if field not in event or event.get(field) in [None, ""]:
            raise ValueError(f"Samachar error: Missing field: {field}")

    # 🚨 ID VALIDATION
    if not isinstance(event["id"], (int, str)):
        raise ValueError("Samachar error: Invalid type for id")

    # 🚨 TIME VALIDATION (FORMAT CHECK)
    if not isinstance(event["time"], str):
        raise ValueError("Samachar error: time must be string")

    try:
        datetime.strptime(event["time"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Samachar error: Invalid timestamp format")

    # 🚨 LAT/LON VALIDATION
    try:
        latitude = float(event["lat"])
        longitude = float(event["lon"])
    except (ValueError, TypeError):
        raise ValueError("Samachar error: lat/lon must be numeric")

    # 🚨 RANGE CHECK (IMPORTANT)
    if not (-90 <= latitude <= 90):
        raise ValueError("Samachar error: latitude out of range")

    if not (-180 <= longitude <= 180):
        raise ValueError("Samachar error: longitude out of range")

    # 🚨 FEATURE TYPE VALIDATION
    feature_type = event["type"]
    if feature_type not in ALLOWED_FEATURE_TYPES:
        raise ValueError("Samachar error: Invalid feature_type")

    # 🚨 VALUE VALIDATION
    value = event.get("value")
    if value is not None and not isinstance(value, (int, float)):
        raise ValueError("Samachar error: value must be number or null")

    # 🚨 DATASET NORMALIZATION
    dataset_id = str(event["dataset_id"])

    # ✅ TRACE ID GENERATION (IMPORTANT)
    trace_id = str(uuid.uuid4())

    # ✅ FINAL MAPPING
    return {
        "signal_id": event["id"],
        "dataset_id": dataset_id,
        "timestamp": event["time"],
        "latitude": latitude,
        "longitude": longitude,
        "feature_type": feature_type,
        "value": value,
        "trace_id": trace_id   # 🔥 ADDED
    }