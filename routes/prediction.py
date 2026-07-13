from fastapi import APIRouter, HTTPException
from database.connection import db
from schemas.predict_schema import PredictRequest
from ml.inference.predict_credit_score import predict_credit_score

router = APIRouter()

@router.post("/predict")
def predict(request: PredictRequest):

    user = db.users.find_one({"email": request.email})

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    credit_data = user.get("credit_input")

    if not credit_data:
        raise HTTPException(
            status_code=400,
            detail="Credit information not found"
        )

    ml_input = {
        "RevolvingUtilizationOfUnsecuredLines": credit_data["credit_utilization"],
        "age": credit_data["age"],
        "NumberOfTime30-59DaysPastDueNotWorse": credit_data["late_30_59"],
        "DebtRatio": credit_data["monthly_debt_payment"],
        "MonthlyIncome": credit_data["monthly_income"],
        "NumberOfOpenCreditLinesAndLoans": credit_data["open_credit_lines"],
        "NumberOfTimes90DaysLate": credit_data["late_90_plus"],
        "NumberRealEstateLoansOrLines": credit_data["real_estate_loans"],
        "NumberOfTime60-89DaysPastDueNotWorse": credit_data["late_60_89"],
        "NumberOfDependents": credit_data["dependents"]
    }

    prediction = predict_credit_score(ml_input)

    db.users.update_one(
        {"email": request.email},
        {
            "$set": {
                "prediction": prediction
            }
        }
    )

    return prediction



@router.get("/dashboard/{email}")
def dashboard(email: str):

    user = db.users.find_one(
        {"email": email},
        {"_id": 0}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user