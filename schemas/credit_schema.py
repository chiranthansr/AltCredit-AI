from pydantic import BaseModel

class CreditInput(BaseModel):
    email: str
    age: int
    monthly_income: float
    monthly_debt_payment: float
    credit_utilization: float
    open_credit_lines: int
    real_estate_loans: int
    late_30_59: int
    late_60_89: int
    late_90_plus: int
    dependents: int