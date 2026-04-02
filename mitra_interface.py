def get_decision(validated_signal):

    status = validated_signal.get("status")
    confidence = validated_signal.get("confidence_score")

    # ❌ REJECT should never reach here (safety check)
    if status == "REJECT":
        raise Exception("REJECTED signal should NEVER reach Mitra")

    # 🟢 ALLOW
    if status == "ALLOW":
        return {
            "status": "ALLOW",
            "risk_level": "LOW",
            "reason": "Signal validated and trusted"
        }

    # 🟡 FLAG
    if status == "FLAG":
        return {
            "status": "FLAG",
            "risk_level": "MEDIUM",
            "reason": "Signal requires review"
        }

    # ⚠ fallback (should not happen)
    return {
        "status": "UNKNOWN",
        "risk_level": "HIGH",
        "reason": "Unexpected status"
    }