from fastapi import APIRouter, HTTPException
from database.connection import db
from schemas.questionnaire_schema import Questionnaire

router = APIRouter()

@router.post("/questionnaire")
def save_questionnaire(data: Questionnaire):

    result = db.users.update_one(
        {"email": data.email},
        {
            "$set": {
                "questionnaire": {
                    "quiz_score": data.quiz_score,
                    "risk_level": data.risk_level
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
        "message": "Questionnaire Saved Successfully"
    }