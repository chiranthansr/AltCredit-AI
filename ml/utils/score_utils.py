def calculate_credit_score(default_probability):
    """
    Convert default probability (0 to 1)
    into a credit score between 300 and 900.
    """

    credit_score = 900 - (default_probability * 600)

    credit_score = round(credit_score)

    return max(300, min(900, credit_score))


def get_risk_level(credit_score):

    if credit_score >= 750:
        return "Low Risk"

    elif credit_score >= 650:
        return "Medium Risk"

    else:
        return "High Risk"


def get_approval_probability(default_probability):

    return float(round((1-default_probability)*100,2))


def get_loan_decision(credit_score):

    if credit_score >= 650:
        return "Approved"

    return "Rejected"