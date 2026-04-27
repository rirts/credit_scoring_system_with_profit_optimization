import pandas as pd
from datetime import datetime
from pathlib import Path

from src.tracking.mappings import ALL_MAPPINGS

LOG_PATH = Path("data/predictions_log.csv")


def enrich_with_mappings(input_data: dict) -> dict:
    enriched = {}

    for key, value in input_data.items():
        # Si existe mapping para esa columna
        if key in ALL_MAPPINGS:
            mapping = ALL_MAPPINGS[key]

            enriched[f"{key}_code"] = value
            enriched[key] = mapping.get(value, "unknown")

        else:
            enriched[key] = value

    return enriched


def log_prediction(input_data: dict, proba: float, decision: int):
    enriched_data = enrich_with_mappings(input_data)

    record = {
        **enriched_data,
        "prediction_proba": float(proba),
        "decision": int(decision),
        "timestamp": datetime.utcnow().isoformat()
    }

    df = pd.DataFrame([record])

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LOG_PATH.exists():
        df.to_csv(LOG_PATH, mode="a", header=False, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(LOG_PATH, index=False, encoding="utf-8-sig")