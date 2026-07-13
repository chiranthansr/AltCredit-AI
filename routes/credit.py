from fastapi import APIRouter, HTTPException
from database.connection import db
from schemas.credit_schema import CreditInput

router = APIRouter()

@router.post("/credit-input")
def save_credit_input(data: CreditInput):

    result = db.users.update_one(
        {"email": data.email},
        {
            "$set": {
                "credit_input": {
                    "age": data.age,
                    "monthly_income": data.monthly_income,
                    "monthly_debt_payment": data.monthly_debt_payment,
                    "credit_utilization": data.credit_utilization,
                    "open_credit_lines": data.open_credit_lines,
                    "real_estate_loans": data.real_estate_loans,
                    "late_30_59": data.late_30_59,
                    "late_60_89": data.late_60_89,
                    "late_90_plus": data.late_90_plus,
                    "dependents": data.dependents
                }
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Credit Information Saved Successfully"
    }