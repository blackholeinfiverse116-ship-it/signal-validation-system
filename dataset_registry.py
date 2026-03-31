# ---------------- DATASET REGISTRY ----------------

DATASET_REGISTRY = {
    "1": {
        "status": "active",
        "trust_score": 0.9,
        "description": "Trusted government dataset"
    },
    "2": {
        "status": "active",
        "trust_score": 0.6,
        "description": "Third-party dataset"
    },
    "3": {
        "status": "inactive",
        "trust_score": 0.4,
        "description": "Deprecated dataset"
    }
}


# ---------------- VALIDATION FUNCTION ----------------

def is_valid_dataset(dataset_id):
    dataset_id = str(dataset_id)
    dataset = DATASET_REGISTRY.get(dataset_id)

    if not dataset:
        return False, "Dataset not found"

    if dataset.get("status") != "active":
        return False, "Dataset is inactive"

    return True, dataset


# ---------------- TRUST SCORE HELPER ----------------

def get_dataset_trust_score(dataset_id):
    dataset_id = str(dataset_id)
    dataset = DATASET_REGISTRY.get(dataset_id)

    if not dataset:
        return 0.0

    return dataset.get("trust_score", 0.0)