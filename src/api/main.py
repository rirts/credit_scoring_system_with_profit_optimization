from fastapi import FastAPI, HTTPException
from src.tracking.logger import log_prediction
from src.monitoring.metrics import (
    load_predictions,
    compute_basic_metrics,
    risk_distribution
)
from src.monitoring.drift import detect_drift
from src.monitoring.alerts import evaluate_alerts
from src.reporting.summary import generate_summary
import pandas as pd
import joblib
import shap
import logging

from src.api.schemas import CreditInput

# Logging primero
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Load artifacts
model = joblib.load("models/model.pkl")
background = joblib.load("models/background.pkl")
THRESHOLD = joblib.load("models/threshold.pkl")

try:
    base_pipeline = model.calibrated_classifiers_[0].estimator

    tree_model = base_pipeline.named_steps['model']
    preprocessor = base_pipeline.named_steps['preprocessor']

    explainer = shap.TreeExplainer(tree_model)

except Exception as e:
    logging.error(f"Error initializing SHAP explainer: {e}")
    explainer = None


@app.get("/")
def root():
    return {"message": "Credit Scoring API running"}


# Predict
@app.post("/predict")
def predict(data: CreditInput):
    try:
        df = pd.DataFrame([data.dict()])
        
        proba = model.predict_proba(df)[0][1]
        prediction = int(proba >= THRESHOLD)

        logging.info(f"Prediction: {proba}")

        # NUEVO: tracking
        log_prediction(
            input_data=data.dict(),
            proba=proba,
            decision=prediction
        )

        return {
            "default_probability": float(proba),
            "prediction": prediction
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Explain
@app.post("/explain")
def explain(data: CreditInput):
    try:
        if explainer is None:
            raise HTTPException(status_code=500, detail="Explainer not initialized")

        df = pd.DataFrame([data.dict()])
        
        # usar preprocessor correcto
        X_transformed = preprocessor.transform(df)

        feature_names = preprocessor.get_feature_names_out()
        
        shap_values = explainer(X_transformed)

        shap_values_array = shap_values.values[0]

        def clean_feature_name(name):
            if "__" in name:
                name = name.split("__")[1]
            if "_" in name:
                parts = name.split("_")
                return f"{parts[0]} = {parts[-1]}"
            return name

        feature_impact = [
            (clean_feature_name(f), v)
            for f, v in zip(feature_names, shap_values_array)
        ]

        # Orden por impacto positivo (riesgo ↑)
        top_positive = sorted(feature_impact, key=lambda x: x[1], reverse=True)[:5]

        # Orden por impacto negativo (riesgo ↓)
        top_negative = sorted(feature_impact, key=lambda x: x[1])[:5]

        top_positive_factors = [
           {"feature": f, "impact": float(v)} for f, v in top_positive
        ]

        top_negative_factors = [
            {"feature": f, "impact": float(v)} for f, v in top_negative
        ]
        
        return {
            "top_positive_factors": top_positive_factors,
            "top_negative_factors": top_negative_factors
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def get_metrics():
    try:
        df = load_predictions()

        basic = compute_basic_metrics(df)
        dist = risk_distribution(df)

        return {
            **basic,
            "risk_distribution": dist
        }

    except FileNotFoundError:
        return {
            "total_predictions": 0,
            "approval_rate": 0.0,
            "average_risk": 0.0,
            "risk_distribution": {}
        }

    except Exception as e:
        logging.error(f"Metrics error: {e}")
        raise HTTPException(status_code=500, detail="Error computing metrics")

@app.get("/drift")
def get_drift():
    try:
        result = detect_drift()
        return result

    except FileNotFoundError:
        return {
            "psi": None,
            "status": "no_data"
        }

    except Exception as e:
        logging.error(f"Drift error: {e}")
        raise HTTPException(status_code=500, detail="Error computing drift")
    
@app.get("/health")
def system_health():
    try:
        df = load_predictions()

        metrics = compute_basic_metrics(df)
        metrics["risk_distribution"] = risk_distribution(df)

        drift = detect_drift()

        alerts = evaluate_alerts(metrics, drift)

        return {
            "metrics": metrics,
            "drift": drift,
            "alerts": alerts,
            "status": "ok" if len(alerts) == 0 else "warning"
        }

    except Exception as e:
        logging.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Error computing system health")

@app.get("/report")
def get_report():
    try:
        df = load_predictions()

        metrics = compute_basic_metrics(df)
        metrics["risk_distribution"] = risk_distribution(df)

        drift = detect_drift()
        alerts = evaluate_alerts(metrics, drift)

        summary = generate_summary(metrics, drift, alerts)

        return {
            "summary": summary["summary"],
            "status": "ok" if len(alerts) == 0 else "warning"
        }

    except Exception as e:
        logging.error(f"Report error: {e}")
        raise HTTPException(status_code=500, detail="Error generating report")