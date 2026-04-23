"""Evaluation module."""
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix

PROFIT_TP = 15000
COST_FN = 10000
COST_FP = 5000

def business_profit(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tp * PROFIT_TP - fn * COST_FN - fp * COST_FP