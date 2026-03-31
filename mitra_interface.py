def send_to_mitra(validated_signal):

    # 🚨 HARD SAFETY CHECK
    if validated_signal["status"] == "REJECT":
        raise Exception("REJECTED signal should NEVER reach Mitra")

    # ✅ FORWARD FULL STANDARDIZED SIGNAL
    return {
        "signal_id": validated_signal["signal_id"],
        "dataset_id": validated_signal["dataset_id"],
        "status": validated_signal["status"],
        "confidence_score": validated_signal["confidence_score"],
        "validation_type": validated_signal["validation_type"],
        "timestamp": validated_signal["timestamp"],
        "trace_id": validated_signal["trace_id"]
    }