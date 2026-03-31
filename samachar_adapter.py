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
            raise Exception(f"Samachar error: Missing field: {field}")

    # 🚨 ID VALIDATION
    if not isinstance(event["id"], (int, str)):
        raise Exception("Samachar error: Invalid type for id")

    # 🚨 TIME VALIDATION
    if not isinstance(event["time"], str):
        raise Exception("Samachar error: time must be string")

    # 🚨 LAT/LON VALIDATION
    try:
        latitude = float(event["lat"])
        longitude = float(event["lon"])
    except (ValueError, TypeError):
        raise Exception("Samachar error: lat/lon must be numeric")

    # 🚨 FEATURE TYPE VALIDATION
    feature_type = event["type"]
    if feature_type not in ALLOWED_FEATURE_TYPES:
        raise Exception("Samachar error: Invalid feature_type")

    # 🚨 VALUE VALIDATION
    value = event.get("value")
    if value is not None and not isinstance(value, (int, float)):
        raise Exception("Samachar error: value must be number or null")

    # 🚨 DATASET NORMALIZATION
    dataset_id = str(event["dataset_id"])

    # ✅ FINAL MAPPING
    return {
        "signal_id": event["id"],
        "dataset_id": dataset_id,
        "timestamp": event["time"],
        "latitude": latitude,
        "longitude": longitude,
        "feature_type": feature_type,
        "value": value
    }
