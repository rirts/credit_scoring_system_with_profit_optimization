import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# Payload REAL basado en tu schema
sample_input = {
    "status": "A11",
    "duration": 12,
    "credit_history": "A32",
    "purpose": "A43",
    "credit_amount": 2500,
    "age": 35,
    "savings": "A61",
    "employment_duration": "A72",
    "installment_rate": 4,
    "personal_status_sex": "A93",
    "other_debtors": "A101",
    "present_residence": 4,
    "property": "A121",
    "other_installment_plans": "A143",
    "housing": "A152",
    "number_of_credits": 2,
    "job": "A173",
    "people_liable": 1,
    "telephone": "A191",
    "foreign_worker": "A201"
}


def test_predict():
    response = client.post("/predict", json=sample_input)
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "default_probability" in data
    assert "prediction" in data
    assert isinstance(data["default_probability"], float)
    assert data["prediction"] in [0, 1]


def test_explain():
    response = client.post("/explain", json=sample_input)
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "top_positive_factors" in data
    assert "top_negative_factors" in data
    assert isinstance(data["shap_values"], list)