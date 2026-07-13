from pydantic import BaseModel

class Consent(BaseModel):
    email: str
    bank_access: bool
    location_access: bool
    questionnaire_access: bool