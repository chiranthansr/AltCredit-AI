import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Keep project-local imports below the sys.path bootstrap so
# direct script runs can still resolve the scripts package.
import joblib
import pandas as pd

from ml.utils.explanation_utils import generate_explanation
from ml.utils.feature_utils import engineer_features
from ml.utils.score_utils import (
    calculate_credit_score,
    get_risk_level,
    get_approval_probability,
    get_loan_decision
)

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "random_forest_credit_model.pkl"
model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents",
    "TotalLatePayments",
    "IncomePerCreditLine",
    "HighDebtFlag",
    "AgeGroup"
]


def predict_credit_score(user_data: dict):
    """
    Predict credit risk for a single user.

    Parameters
    ----------
    user_data : dict
        Dictionary containing the user's financial information.

    Returns
    -------
    dict
        Prediction result and default probability.
    """

    # Convert dictionary to DataFrame
    input_df = pd.DataFrame([user_data])

    # Apply feature engineering
    input_df = engineer_features(input_df)

    input_df = input_df[FEATURE_ORDER]

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Probability of default (class = 1)
    default_probability = model.predict_proba(input_df)[0][1]

    credit_score = calculate_credit_score(default_probability)

    risk_level = get_risk_level(credit_score)

    approval_probability = get_approval_probability(
        default_probability
    )

    loan_decision = get_loan_decision(
        credit_score
    )
    explanations = generate_explanation(user_data)

    return {

    "credit_score": credit_score,

    "risk_level": risk_level,

    "default_probability": round(
        float(default_probability) * 100,2),

        "approval_probability": float(approval_probability),

        "loan_decision": loan_decision,

        "explanations": explanations
    }


if __name__ == "__main__":

    sample_user = {
        "RevolvingUtilizationOfUnsecuredLines": 0.25,
        "age": 35,
        "NumberOfTime30-59DaysPastDueNotWorse": 0,
        "DebtRatio": 0.40,
        "MonthlyIncome": 50000,
        "NumberOfOpenCreditLinesAndLoans": 6,
        "NumberOfTimes90DaysLate": 0,
        "NumberRealEstateLoansOrLines": 1,
        "NumberOfTime60-89DaysPastDueNotWorse": 0,
        "NumberOfDependents": 2
    }

    result = predict_credit_score(sample_user)

    print("Prediction Result")
    print(result)
