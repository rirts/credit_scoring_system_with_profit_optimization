def generate_summary(metrics, drift, alerts):
    approval = metrics["approval_rate"]
    risk = metrics["average_risk"]

    # --- Base message ---
    if len(alerts) == 0:
        status_msg = "The system is operating normally."
    else:
        status_msg = "The system requires attention due to detected issues."

    # --- Approval interpretation ---
    if approval < 0.3:
        approval_msg = "Approval rate is low, indicating strict risk control."
    elif approval > 0.8:
        approval_msg = "Approval rate is high, potential risk exposure."
    else:
        approval_msg = "Approval rate is within a balanced range."

    # --- Risk interpretation ---
    if risk > 0.6:
        risk_msg = "Portfolio risk is elevated."
    elif risk < 0.3:
        risk_msg = "Portfolio risk is low."
    else:
        risk_msg = "Portfolio risk is moderate."

    # --- Drift interpretation ---
    drift_status = drift.get("status", "unknown")

    if drift_status == "stable":
        drift_msg = "No significant changes in data distribution."
    elif drift_status == "moderate_drift":
        drift_msg = "Some changes detected in data distribution."
    elif drift_status == "significant_drift":
        drift_msg = "Significant data drift detected."
    else:
        drift_msg = "Not enough data to evaluate drift."

    return {
        "summary": f"{status_msg} {approval_msg} {risk_msg} {drift_msg}"
    }