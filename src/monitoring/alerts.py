def evaluate_alerts(metrics, drift):
    alerts = []

    # --- Drift ---
    if drift["status"] == "significant_drift":
        alerts.append({
            "type": "drift",
            "level": "high",
            "message": "Significant drift detected"
        })
    elif drift["status"] == "moderate_drift":
        alerts.append({
            "type": "drift",
            "level": "medium",
            "message": "Moderate drift detected"
        })

    # --- Approval rate ---
    approval = metrics["approval_rate"]

    if approval < 0.3:
        alerts.append({
            "type": "approval_rate",
            "level": "high",
            "message": "Approval rate too low"
        })
    elif approval > 0.9:
        alerts.append({
            "type": "approval_rate",
            "level": "medium",
            "message": "Approval rate unusually high"
        })

    # --- Risk level ---
    risk = metrics["average_risk"]

    if risk > 0.6:
        alerts.append({
            "type": "risk",
            "level": "high",
            "message": "Portfolio risk is high"
        })

    return alerts