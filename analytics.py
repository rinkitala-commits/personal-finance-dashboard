def total_income(df):
    return df["Income"].sum()


def total_expense(df):
    return df["Expense"].sum()


def balance(df):
    return total_income(df) - total_expense(df)


def savings_rate(df):
    income = total_income(df)

    if income == 0:
        return 0

    return (balance(df) / income) * 100


def expense_percentage(df):
    income = total_income(df)

    if income == 0:
        return 0

    return (total_expense(df) / income) * 100

def expense_by_category(df):
    """
    Returns only categories with actual expenses.
    """
    return (
        df.groupby("Category")["Expense"]
        .sum()
        .loc[lambda x: x > 0]
        .sort_values(ascending=False)
    )


def income_by_category(df):
    """
    Returns total income grouped by category.
    """
    return (
        df.groupby("Category")["Income"]
        .sum()
        .sort_values(ascending=False)
    )

import pandas as pd

def monthly_summary(df):
    """
    Generate complete monthly financial summary.
    """

    df = df.copy()

    df["Month"] = (
        df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    summary = (
        df.groupby("Month")
        .agg(
            Income=("Income", "sum"),
            Expenses=("Expense", "sum"),
            Transactions=("Date", "count")
        )
    )

    summary["Savings"] = (
        summary["Income"]
        - summary["Expenses"]
    )

    summary["Savings Rate (%)"] = (
        summary["Savings"]
        / summary["Income"]
        * 100
    ).fillna(0).round(2)

    summary["Expense Percentage (%)"] = (
        summary["Expenses"]
        / summary["Income"]
        * 100
    ).fillna(0).round(2)

    return summary

def transaction_statistics(df, total_income, total_expense):
    """
    Calculate transaction statistics.
    """

    stats = {}

    # Average Daily Expense
    days = df["Date"].dt.date.nunique()

    if days > 0:
        stats["average_daily_expense"] = total_expense / days
    else:
        stats["average_daily_expense"] = 0

    # Expense Transactions
    expense_transactions = df[df["Expense"] > 0]

    if not expense_transactions.empty:
        stats["highest_expense"] = expense_transactions["Expense"].max()
        stats["lowest_expense"] = expense_transactions["Expense"].min()
    else:
        stats["highest_expense"] = 0
        stats["lowest_expense"] = 0

    # Income Transactions
    income_transactions = df[df["Income"] > 0]

    if not income_transactions.empty:
        stats["highest_income"] = income_transactions["Income"].max()
        stats["lowest_income"] = income_transactions["Income"].min()
    else:
        stats["highest_income"] = 0
        stats["lowest_income"] = 0

    # Average Transaction
    stats["average_transaction"] = df["Amount"].mean()

    # Expense / Income Ratio
    if total_income > 0:
        stats["expense_income_ratio"] = (
            total_expense / total_income
        ) * 100
    else:
        stats["expense_income_ratio"] = 0

    return stats