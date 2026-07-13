import pandas as pd


def engineer_features(df):

    df["TotalLatePayments"] = (
        df["NumberOfTime30-59DaysPastDueNotWorse"]
        + df["NumberOfTime60-89DaysPastDueNotWorse"]
        + df["NumberOfTimes90DaysLate"]
    )

    df["IncomePerCreditLine"] = (
        df["MonthlyIncome"]
        /
        (df["NumberOfOpenCreditLinesAndLoans"] + 1)
    )

    df["HighDebtFlag"] = (
        df["DebtRatio"] > 1
    ).astype(int)

    df["AgeGroup"] = pd.cut(
        df["age"],
        bins=[18, 30, 50, float("inf")],
        labels=[0, 1, 2]
    ).astype(int)

    return df