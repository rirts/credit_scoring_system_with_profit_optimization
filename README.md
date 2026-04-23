# Credit Scoring System with Profit Optimization

An end-to-end machine learning system for credit risk modeling, designed to align predictive performance with **real financial outcomes**.

This project goes beyond traditional classification by optimizing decisions based on **expected profit**, while ensuring explainability, fairness, and production readiness.

## Problem Statement

Financial institutions must balance two competing risks:

- Approving high-risk clients → financial loss (defaults)
- Rejecting low-risk clients → lost revenue

Most ML models optimize for accuracy or AUC, which **do not reflect real business impact**.

This project addresses that gap by building a system that:

- Predicts probability of default
- Optimizes decision thresholds based on profit
- Explains decisions using SHAP
- Evaluates and mitigates fairness risks
- Deploys the model via a FastAPI API

## Key Results
Key results depend on the trained model and may vary across runs.

In the latest training cycle:

- Optimized threshold: ~0.18
- Approval rate: ~65–70%
- Default rate: ~10–15%
- Positive expected profit under business constraints

The system is designed to **adapt dynamically** based on data and cost assumptions, rather than relying on fixed thresholds.

## Business Case Simulation

We evaluate three representative customer profiles:

### Low-Risk Customer

- Default probability: ~0.5%
- Decision: APPROVED

The model identifies strong financial stability (low exposure, good credit history), leading to confident approvals.

### High-Risk Customer

- Default probability: ~65%
- Decision: REJECTED

Risk is driven by long credit duration and unstable financial indicators, which significantly increase expected loss.

### Borderline Customer

- Default probability: ~24%
- Decision: REJECTED

Although not clearly high-risk, the model rejects this profile due to expected financial loss.

This highlights a key design choice:

The system favors **profitability over approval rate**, rejecting borderline cases that traditional models might accept.

### Explainability Insights (SHAP)

Each decision is supported by feature-level explanations:

- Low-risk customers show strong negative contributions from features such as:
  - Short duration
  - Low credit amount
  - Strong credit history

- High-risk customers are driven by:
  - Long duration
  - Higher credit exposure
  - Weak financial indicators

- Borderline cases highlight trade-offs:
  - Some features push toward approval
  - Others increase risk, leading to rejection under profit optimization

This allows analysts to **justify individual credit decisions**, not just predict them.

## Dataset

German Credit Dataset (UCI ML Repository):

- 1000 observations
- 20 variables (numerical + categorical)
- Binary target (default / no default)

## Project Structure

credit_scoring_project/
├── data/
├── notebooks/
├── src/
│ ├── data/
│ ├── features/
│ ├── models/
│ ├── evaluation/
│ └── api/
├── models/
├── reports/
├── tests/

### Workflow
Raw data → preprocessing → feature engineering → modeling → calibration → threshold optimization → fairness → API deployment

## ML Pipeline

- Data preprocessing (scaling + encoding)
- Logistic Regression (baseline)
- XGBoost (tuned model)
- Probability calibration (isotonic)
- Profit-driven threshold optimization
- Cross-validation for threshold stability
- Fairness evaluation and mitigation
- SHAP-based explainability

## Model Performance

|         Model        |  AUC | Recall | Precision |   Business Impact  |
|          ---         |  --- |   ---  |    ---    |         ---        |
|  Logistic Regression | 0.80 |  0.53  |    0.68   |      Baseline      |
| XGBoost (calibrated) | 0.85 |  0.77  |    0.62   |  Profit-optimized  |

**Key trade-off**: Recall improved significantly (0.53 → 0.77), reducing missed defaults, at the cost of more conservative approvals.

## Explainability (SHAP)

SHAP is used to provide **individual-level explanations**.

Key drivers of risk:

- Higher credit amount → increases default probability
- Longer loan duration → increases risk
- Strong credit history → reduces risk

This enables transparent decision-making for both analysts and stakeholders.

## Fairness Analysis

Metrics evaluated:

- Demographic Parity
- Equal Opportunity

Findings:

- Higher rejection rates among younger applicants
- Similar risk detection performance across groups

Mitigation:

- Group-specific thresholds reduced disparities
- Trade-off: slight increase in risk, but improved fairness

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

**Example Request:**
``` bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"status":"A11","duration":12,"credit_amount":2500,"age":35,...}'
```
**Example Response:**
``` json
{
  "default_probability": 0.38,
  "prediction": 1
}
```

### API Architecture

- FastAPI-based service
- Pre-trained pipeline loaded via joblib
- Probability calibration handled inside the model
- SHAP TreeExplainer for real-time explainability

Endpoints:

- `/predict`
  - Input: raw customer features
  - Output: probability of default + decision

- `/explain`
  - Input: same payload
  - Output: top positive and negative feature contributions

The API simulates a real-world credit decision engine, enabling both prediction and interpretability in production.

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

- Threshold recalibration required if business costs change
- Model performance depends on data distribution stability
- SHAP explanations depend on the underlying tree model
- Fairness interventions may impact profitability

Potential extensions:

- Model monitoring (data drift, prediction drift)
- Automated retraining pipelines
- Feature store integration
- A/B testing for threshold strategies

## Conclusion

This project demonstrates how to move from a traditional ML model to a **decision system aligned with business objectives**.

Instead of optimizing for accuracy, the system:

- Optimizes decisions based on profit
- Explains outcomes at the individual level
- Evaluates fairness trade-offs
- Is deployable as a real API service

This reflects how modern credit risk systems operate in practice, where **decision quality matters more than model metrics**.