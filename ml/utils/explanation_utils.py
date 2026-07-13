def generate_explanation(user_data):

    explanations = []

    # Debt Ratio
    if user_data["DebtRatio"] < 0.5:
        explanations.append(
            "Low debt ratio improved the credit score."
        )
    else:
        explanations.append(
            "High debt ratio increased financial risk."
        )

    # Income
    if user_data["MonthlyIncome"] >= 50000:
        explanations.append(
            "Stable monthly income increased creditworthiness."
        )
    else:
        explanations.append(
            "Lower income slightly reduced the score."
        )

    # Late Payments
    total_late = (
        user_data["NumberOfTime30-59DaysPastDueNotWorse"]
        +
        user_data["NumberOfTime60-89DaysPastDueNotWorse"]
        +
        user_data["NumberOfTimes90DaysLate"]
    )

    if total_late == 0:
        explanations.append(
            "No recent late payments reduced default risk."
        )
    else:
        explanations.append(
            "Previous late payments negatively affected the score."
        )

    # Credit Utilization
    if user_data["RevolvingUtilizationOfUnsecuredLines"] < 0.30:
        explanations.append(
            "Low credit utilization positively influenced the score."
        )
    else:
        explanations.append(
            "High credit utilization increased the overall risk."
        )

    return explanations