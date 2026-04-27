# src/tracking/mappings.py

STATUS_MAP = {
    "A11": "< 0 DM",
    "A12": "0–200 DM",
    "A13": ">= 200 DM",
    "A14": "no checking account"
}

CREDIT_HISTORY_MAP = {
    "A30": "no credits taken",
    "A31": "all credits paid back",
    "A32": "existing credits paid back",
    "A33": "delay in paying past",
    "A34": "critical account"
}

PURPOSE_MAP = {
    "A40": "car (new)",
    "A41": "car (used)",
    "A42": "furniture/equipment",
    "A43": "radio/TV",
    "A44": "domestic appliances",
    "A45": "repairs",
    "A46": "education",
    "A47": "vacation",
    "A48": "retraining",
    "A49": "business",
    "A410": "others"
}

SAVINGS_MAP = {
    "A61": "< 100 DM",
    "A62": "100–500 DM",
    "A63": "500–1000 DM",
    "A64": ">= 1000 DM",
    "A65": "unknown / no savings"
}

EMPLOYMENT_MAP = {
    "A71": "unemployed",
    "A72": "< 1 year",
    "A73": "1–4 years",
    "A74": "4–7 years",
    "A75": ">= 7 years"
}

PERSONAL_STATUS_MAP = {
    "A91": "male divorced/separated",
    "A92": "female divorced/separated/married",
    "A93": "male single",
    "A94": "male married/widowed",
    "A95": "female single"
}

DEBTORS_MAP = {
    "A101": "none",
    "A102": "co-applicant",
    "A103": "guarantor"
}

PROPERTY_MAP = {
    "A121": "real estate",
    "A122": "building society savings",
    "A123": "car or other",
    "A124": "unknown"
}

INSTALLMENT_PLANS_MAP = {
    "A141": "bank",
    "A142": "stores",
    "A143": "none"
}

HOUSING_MAP = {
    "A151": "rent",
    "A152": "own",
    "A153": "free"
}

JOB_MAP = {
    "A171": "unemployed / unskilled non-resident",
    "A172": "unskilled resident",
    "A173": "skilled employee",
    "A174": "management / highly qualified"
}

TELEPHONE_MAP = {
    "A191": "none",
    "A192": "yes"
}

FOREIGN_WORKER_MAP = {
    "A201": "yes",
    "A202": "no"
}


ALL_MAPPINGS = {
    "status": STATUS_MAP,
    "credit_history": CREDIT_HISTORY_MAP,
    "purpose": PURPOSE_MAP,
    "savings": SAVINGS_MAP,
    "employment_duration": EMPLOYMENT_MAP,
    "personal_status_sex": PERSONAL_STATUS_MAP,
    "other_debtors": DEBTORS_MAP,
    "property": PROPERTY_MAP,
    "other_installment_plans": INSTALLMENT_PLANS_MAP,
    "housing": HOUSING_MAP,
    "job": JOB_MAP,
    "telephone": TELEPHONE_MAP,
    "foreign_worker": FOREIGN_WORKER_MAP
}