from fastapi import FastAPI, HTTPException
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

# 🔥 FIX CLAVE: acceder correctamente al modelo interno
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