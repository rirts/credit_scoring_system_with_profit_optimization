# Credit Decision System with Profit Optimization

An end-to-end credit decision system that separates **risk estimation, decision policy, and business strategy**.

Instead of optimizing for accuracy, the system maximizes **expected profit**, enabling different lending strategies (conservative, balanced, growth) using the same model.

Key Capabilities:
- Probability of default estimation (calibrated XGBoost)
- Profit-driven decision policy (threshold optimization)
- Monitoring and drift detection (PSI)
- Alerting and system health checks
- Explainability (SHAP)
- Fairness evaluation and mitigation
- Production-ready API (FastAPI)

The key idea: **model performance alone is not enough, decisions must be aligned with business objectives.**

## Problem Statement

Credit decisions involve a fundamental trade-off:

- Approving risky clients leads to financial losses  
- Rejecting good clients leads to missed revenue  

Traditional ML models optimize metrics like AUC, but **do not directly translate predictions into business decisions**.

This system addresses that gap by explicitly separating:

- Risk estimation (probability of default)  
- Decision policy (threshold optimization)  
- Business context (costs and profit)  

This enables decisions that are directly aligned with financial outcomes.

## System Architecture

The system is designed as a modular decision engine:

1. **Risk Model**
   - Predicts probability of default using a calibrated XGBoost model

2. **Decision Policy**
   - Applies a threshold optimized for expected profit
   - Can be adjusted to reflect different business strategies

3. **Monitoring Layer**
   - Tracks predictions over time
   - Computes approval rate, risk distribution, and portfolio metrics

4. **Drift Detection**
   - Uses Population Stability Index (PSI) to detect distribution changes
   - Prevents unreliable conclusions with minimum sample thresholds

5. **Alerting System**
   - Triggers warnings based on drift and business KPIs

6. **Reporting Layer**
   - Translates system behavior into business-readable summaries

This separation allows the same model to behave differently depending on business context.

## How It Works (End-to-End)

1. A customer request is sent to the API (`/predict`)
2. The model estimates probability of default
3. A profit-optimized threshold is applied
4. The decision (approve/reject) is returned
5. The prediction is logged and stored for monitoring
6. Monitoring endpoints expose system performance in real time
7. Health checks evaluate drift and operational risk
8. A business summary can be retrieved via `/report`

This simulates a real-world credit decision flow, from prediction to monitoring.

## Example Usage

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"status":"A11","duration":12,"credit_amount":2500,"age":35,...}'
```
```json
{
  "default_probability": 0.38,
  "prediction": 1
}
```

**Interpretation:**
- `default_probability` → estimated probability of default
- `prediction = 1` → client classified as high risk (rejected)
- `prediction = 0` → client classified as low risk (approved)

## Key Results

In the latest training cycle:

- Decision threshold: ~0.18 (profit-optimized)
- Approval rate: ~65–70%
- Default rate: ~10–15%
- Positive expected profit under baseline assumptions

The system maintains stable decision behavior across cross-validation folds (low threshold variance), indicating robustness.

Results are not tied to a fixed threshold, the system adapts dynamically to data and business cost structures.

## Business Case Simulation

The system was tested on three representative profiles:

- **Low-risk customer (~0.5%)** → Approved  
- **High-risk customer (~65%)** → Rejected  
- **Borderline customer (~24%)** → Rejected  

This highlights a key behavior:

The system prioritizes **profitability over approval rate**, rejecting borderline cases when expected loss outweighs potential gain.

## Dataset

The system is built on the German Credit dataset (UCI Repository), containing:

- 1000 observations
- 20 features (categorical + numerical)
- Binary target (default / no default)

While the dataset is relatively small, the focus of this project is not on scale, but on:

- Decision system design  
- Business-driven optimization  
- Production-style architecture  

The same system can be extended to larger, real-world datasets without changes in design.

## Project Structure

```bash
credit_scoring_project/
├── data/              # raw and processed datasets
├── notebooks/         # EDA and experimentation
├── src/
│   ├── data/          # data loading
│   ├── features/      # feature engineering
│   ├── models/        # training pipeline
│   ├── evaluation/    # business metrics
│   └── api/           # FastAPI service
├── models/            # serialized artifacts
├── reports/           # monitoring outputs and business summaries
├── tests/             # API tests
```

## Model Artifacts

The system persists key artifacts generated during training:

- `models/model.pkl` → calibrated model (XGBoost + calibration)
- `models/preprocessor.pkl` → feature transformation pipeline
- `models/threshold.pkl` → profit-optimized decision threshold
- `models/train_scores.pkl` → training probability distribution (baseline for drift)
- `models/background.pkl` → SHAP background dataset

These artifacts decouple training from inference, enabling reproducible and consistent predictions in production.

### Workflow
Raw data → preprocessing → feature engineering → modeling → calibration → threshold optimization → fairness → API deployment

## Model Performance

|         Model        |  AUC | Recall | Precision |   Business Impact  |
|          ---         |  --- |   ---  |    ---    |         ---        |
|  Logistic Regression | 0.80 |  0.53  |    0.68   |      Baseline      |
| XGBoost (calibrated) | 0.85 |  0.77  |    0.62   |  Profit-optimized  |

**Key trade-off**: Recall improved significantly (0.53 → 0.77), reducing missed defaults, at the cost of more conservative approvals.

## Model Transparency

### Explainability (SHAP)

The system provides feature-level explanations for each decision:

- Higher credit amount → increases risk  
- Longer duration → increases risk  
- Strong credit history → reduces risk  

This enables analysts to justify individual decisions.

### Fairness

The system evaluates fairness across demographic groups:

- Higher rejection rates among younger applicants  
- Similar risk detection performance across groups  

Mitigation:

- Group-specific thresholds reduce disparities  
- Trade-off: slight increase in risk for improved fairness

## Threshold Optimization
Instead of using a default threshold (0.5), the system selects a threshold that maximizes profit.

- Optimized threshold: dynamically estimated (~0.18 in latest run)
- Stability: low variance across cross-validation folds (std < 0.05)

The threshold is not fixed and is recalculated during training to reflect current data and business costs.

## Business Simulation & Stress Testing
- Approval rate: ~65–70%
- Default rate: ~10–15%
- Positive expected profit under baseline conditions

Under stress scenarios (higher default costs):

- Profit decreases but remains positive
- The model maintains stability under adverse conditions

## API Deployment (FastAPI)

Endpoints:

- `POST /predict` → Returns default probability and decision

- `POST /explain` → Returns top SHAP feature contributions

### API Architecture

- FastAPI-based service
- Pre-trained pipeline loaded via joblib
- Probability calibration handled inside the model
- SHAP TreeExplainer for real-time explainability

### Core Endpoints

- `POST /predict`  
  Returns:
  - probability of default
  - approval / rejection decision

- `POST /explain`  
  Returns:
  - top positive risk drivers
  - top negative risk drivers

### Monitoring Endpoints

- `GET /metrics`  
  Returns:
  - total predictions
  - approval rate
  - average portfolio risk
  - risk distribution

- `GET /health`  
  Returns:
  - system status
  - drift analysis
  - active alerts

- `GET /report`  
  Returns:
  - business-readable system summary

The API exposes both:

- **Decision services** for real-time credit evaluation
- **Operational services** for monitoring model behavior in production

This mirrors how production ML systems separate prediction from observability.

### Monitoring Logic

- Metrics are computed on accumulated predictions (not per request)
- Drift detection (PSI) is only evaluated when sufficient data is available
- Alerts are triggered based on:
  - abnormal approval rate
  - elevated portfolio risk
  - significant distribution drift
- Predictions are stored in-memory for monitoring purposes (can be extended to persistent storage)

This prevents noisy signals and ensures reliable monitoring decisions.

## Run Locally

```bash
git clone <repo>
cd credit_scoring_project

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn src.api.main:app --reload
```

## Production Considerations

- Current monitoring layer simulates production behavior; persistence and scheduling can be added for full deployment
- Model performance depends on data distribution stability (monitored via PSI)
- Decision thresholds must be aligned with business costs and can be recalibrated
- Monitoring endpoints provide visibility into approval rate and portfolio risk
- Alerting system highlights anomalies in real time
- Drift detection prevents silent model degradation

Potential extensions:
- Automated retraining pipelines triggered by drift
- Dashboard for executive monitoring
- Champion/Challenger model comparison

## Conclusion

This project demonstrates how to move from a predictive model to a **production-style decision system**.

Instead of optimizing for accuracy, it:

- Aligns decisions with financial outcomes  
- Separates modeling from business strategy  
- Provides monitoring, drift detection, and alerting  
- Translates technical outputs into business insights  

This reflects how modern data systems operate in practice:  
**models do not create value, decision systems do.**

## System Design Philosophy

The system is built around a key principle:

A model is only one component of a decision system.

By separating:

- prediction (risk)
- decision logic (threshold)
- business assumptions (costs)

the system becomes flexible, interpretable, and aligned with real-world operations.

This design allows the same model to support multiple strategies without retraining.

## Limitations

- Small dataset (1000 observations) limits generalization
- Proxy variables used for fairness analysis may not reflect real demographics
- Drift detection is based on prediction distribution, not raw feature drift
- Business cost assumptions are static and may change over time

These limitations reflect real-world challenges and highlight areas for future improvement.