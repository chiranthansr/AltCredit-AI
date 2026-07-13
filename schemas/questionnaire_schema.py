from pydantic import BaseModel

class Questionnaire(BaseModel):
    email: str
    quiz_score: int
    risk_level: str