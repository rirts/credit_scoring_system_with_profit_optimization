import pandas as pd

COLUMNS = [
    "status", "duration", "credit_history", "purpose",
    "credit_amount", "savings", "employment_duration",
    "installment_rate", "personal_status_sex", "other_debtors",
    "present_residence", "property", "age",
    "other_installment_plans", "housing",
    "number_of_credits", "job", "people_liable",
    "telephone", "foreign_worker", "target"
]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=' ', header=None)
    df.columns = COLUMNS
    return df