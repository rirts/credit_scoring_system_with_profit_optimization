from pydantic import BaseModel
from typing import Literal

class CreditInput(BaseModel):
    status: Literal['A11', 'A12', 'A13', 'A14']
    duration: int
    credit_history: Literal['A30','A31','A32','A33','A34']
    purpose: str
    credit_amount: int
    savings: str
    employment_duration: str
    installment_rate: int
    personal_status_sex: str
    other_debtors: str
    present_residence: int
    property: str
    age: int
    other_installment_plans: str
    housing: Literal['A151','A152','A153']
    number_of_credits: int
    job: str
    people_liable: int
    telephone: str
    foreign_worker: str