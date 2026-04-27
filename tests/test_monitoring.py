from src.monitoring.metrics import load_predictions, compute_basic_metrics, risk_distribution

df = load_predictions()

print("=== BASIC METRICS ===")
print(compute_basic_metrics(df))

print("\n=== RISK DISTRIBUTION ===")
print(risk_distribution(df))