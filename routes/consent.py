from fastapi import APIRouter, HTTPException
from database.connection import db
from schemas.consent_schema import Consent

router = APIRouter()

@router.post("/consent")
def save_consent(consent: Consent):

    result = db.users.update_one(
        {"email": consent.email},
        {
            "$set": {
                "consent": {
                    "bank_access": consent.bank_access,
                    "location_access": consent.location_access,
                    "questionnaire_access": consent.questionnaire_access
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
        "message": "Consent Saved Successfully"
    }