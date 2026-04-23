import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix
from sklearn.base import clone

from xgboost import XGBClassifier

from src.data.load_data import load_data

# Paths
DATA_PATH = "data/raw/german.data"
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

# Business parameters
PROFIT_TP = 15000
COST_FN = 10000
COST_FP = 5000

def business_profit(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tp * PROFIT_TP - fn * COST_FN - fp * COST_FP

def optimize_threshold(y_true, y_proba):
    best_t = 0
    best_profit = -np.inf

    for t in np.linspace(0.01, 0.99, 100):
        y_pred = (y_proba >= t).astype(int)
        profit = business_profit(y_true, y_pred)

        if profit > best_profit:
            best_profit = profit
            best_t = t

    return best_t

def threshold_stability(X, y, model):
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    thresholds = []

    for train_idx, val_idx in skf.split(X, y):
        model_clone = clone(model)

        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model_clone.fit(X_tr, y_tr)
        y_proba = model_clone.predict_proba(X_val)[:, 1]

        t = optimize_threshold(y_val, y_proba)
        thresholds.append(t)

    return np.median(thresholds)

def train():
    print("Loading data...")
    df = load_data(DATA_PATH)
    df['target'] = df['target'].map({1: 0, 2: 1})

    X = df.drop(columns=['target'])
    y = df['target']

    num_cols = X.select_dtypes(include='number').columns.tolist()
    cat_cols = X.select_dtypes(exclude='number').columns.tolist()

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', XGBClassifier(
            random_state=42,
            eval_metric='logloss'
        ))
    ])

    print("Training model...")
    calibrated_model = CalibratedClassifierCV(
        pipeline,
        method='isotonic',
        cv=5
    )

    calibrated_model.fit(X, y)

    print("Optimizing threshold...")
    threshold = threshold_stability(X, y, calibrated_model)

    print(f"Final threshold: {threshold:.3f}")

    print("Saving artifacts...")

    joblib.dump(calibrated_model, MODEL_DIR / "model.pkl")
    joblib.dump(threshold, MODEL_DIR / "threshold.pkl")

    # SHAP background
    sample = X.sample(100, random_state=42)
    transformed = pipeline.named_steps['preprocessor'].fit(X).transform(sample)

    joblib.dump(transformed, MODEL_DIR / "background.pkl")

    print("Training complete.")

if __name__ == "__main__":
    train()