import pandas as pd
from pathlib import Path

LOG_PATH = Path("data/predictions_log.csv")


def load_predictions():
    if not LOG_PATH.exists():
        raise FileNotFoundError("No prediction log found")
    
    df = pd.read_csv(LOG_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    return df


def compute_basic_metrics(df: pd.DataFrame):
    total = len(df)
    approvals = int(df["decision"].sum())
    
    approval_rate = float(approvals / total) if total > 0 else 0.0
    avg_risk = float(df["prediction_proba"].mean())

    return {
        "total_predictions": int(total),
        "approval_rate": round(approval_rate, 4),
        "average_risk": round(avg_risk, 4)
    }


def risk_distribution(df: pd.DataFrame):
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
    labels = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]

    df["risk_bucket"] = pd.cut(df["prediction_proba"], bins=bins, labels=labels)

    distribution = df["risk_bucket"].value_counts().sort_index()

    # Convertir a dict limpio
    return {str(k): int(v) for k, v in distribution.items()}