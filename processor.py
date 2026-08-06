import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/transactions.csv")

print(df)

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Dataset Information ---")
print(df.info())

print("\n--- Column Names ---")
print(df.columns)

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Basic Statistics ---")
print(df.describe())

# Check category distribution
print("\n--- Category Distribution ---")
print(df["Category"].value_counts())

# Display the complete dataset
print("\n--- Complete Dataset ---")
print(df)

# Clean category names
df["Category"] = df["Category"].replace("Billse", "Bills")

print("\n--- Cleaned Categories ---")
print(df["Category"].value_counts())

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("\n--- Date Data Type After Conversion ---")
print(df["Date"].dtype)

# Check cleaned dataset
print("\n--- Cleaned Dataset ---")
print(df)

# Create Income and Expense columns
df["Income"] = df["Amount"].apply(lambda x: x if x > 0 else 0)
df["Expense"] = df["Amount"].apply(lambda x: abs(x) if x < 0 else 0)

print("\n--- Income and Expense ---")
print(df[["Description", "Amount", "Income", "Expense"]])

# Calculate total income
total_income = df["Income"].sum()

print("\n--- Total Income ---")
print(total_income)

# Calculate total expenses
total_expense = df["Expense"].sum()

print("\n--- Total Expenses ---")
print(total_expense)

# Calculate balance
balance = total_income - total_expense

print("\n--- Balance ---")
print(balance)

# Calculate expenses by category
expense_by_category = df.groupby("Category")["Expense"].sum()

print("\n--- Expenses by Category ---")
print(expense_by_category)

# Find the category with the highest expense
highest_expense_category = expense_by_category.idxmax()
highest_expense_amount = expense_by_category.max()

print("\n--- Highest Expense Category ---")
print("Category:", highest_expense_category)
print("Amount:", highest_expense_amount)

# Find the largest single expense
largest_expense = df["Expense"].max()

print("\n--- Largest Single Expense ---")
print("Amount:", largest_expense)

# Find the transaction with the largest expense
largest_expense_row = df.loc[df["Expense"].idxmax()]

print("\n--- Largest Expense Transaction ---")
print("Description:", largest_expense_row["Description"])
print("Amount:", largest_expense_row["Expense"])
print("Category:", largest_expense_row["Category"])

# Count total transactions
total_transactions = len(df)

print("\n--- Total Transactions ---")
print(total_transactions)

# Calculate average expense
average_expense = df.loc[df["Expense"] > 0, "Expense"].mean()

print("\n--- Average Expense ---")
print(average_expense)

# Calculate average income
average_income = df.loc[df["Income"] > 0, "Income"].mean()

print("\n--- Average Income ---")
print(average_income)

# Calculate savings rate
savings_rate = (balance / total_income) * 100

print("\n--- Savings Rate ---")
print(savings_rate)

#Round savings rate to 2 decimal places
savings_rate_rounded = round(savings_rate, 2)

print("\n--- Rounded Savings Rate ---")
print(savings_rate_rounded)


# Calculate expense percentage
expense_percentage = (total_expense / total_income) * 100

print("\n--- Expense Percentage ---")
print(expense_percentage)

#Round expense percentage to 2 decimal places
expense_percentage_rounded = round(expense_percentage, 2)   

print("\n--- Rounded Expense Percentage ---")
print(expense_percentage_rounded)

# Count income transactions
income_transactions = (df["Income"] > 0).sum()

print("\n--- Income Transactions ---")
print(income_transactions)

# Count expense transactions
expense_transactions = (df["Expense"] > 0).sum()

print("\n--- Expense Transactions ---")
print(expense_transactions)

# Find the largest income transaction
largest_income = df["Income"].max()

print("\n--- Largest Income Transaction ---")
print("Amount:", largest_income)

# Find the transaction with the largest income
largest_income_row = df.loc[df["Income"].idxmax()]

print("\n--- Largest Income Transaction Details ---")
print("Description:", largest_income_row["Description"])
print("Amount:", largest_income_row["Income"])
print("Category:", largest_income_row["Category"])

# Calculate expenses by category, excluding Income
expense_by_category = df[df["Expense"] > 0].groupby("Category")["Expense"].sum()

print("\n--- Spending by Category ---")
print(expense_by_category)

# Find the top 3 spending categories
top_3_categories = expense_by_category.sort_values(ascending=False).head(3)

print("\n--- Top 3 Spending Categories ---")
print(top_3_categories)

# Calculate spending percentage for each category
category_percentage = (expense_by_category / total_expense) * 100

print("\n--- Category Spending Percentage ---")
print(category_percentage)

# Sort categories by spending percentage
category_percentage_sorted = category_percentage.sort_values(ascending=False)

print("\n--- Spending Percentage by Category ---")
print(category_percentage_sorted)

# Round category percentages to 2 decimal places
category_percentage_rounded = category_percentage_sorted.round(2)

print("\n--- Rounded Spending Percentage ---")
print(category_percentage_rounded)

# Find the category with the highest spending percentage
highest_percentage_category = category_percentage_rounded.idxmax()
highest_percentage = category_percentage_rounded.max()

print("\n--- Highest Spending Percentage ---")
print("Category:", highest_percentage_category)
print("Percentage:", highest_percentage)

# Calculate balance percentage
balance_percentage = (balance / total_income) * 100

print("\n--- Balance Percentage ---")
print(balance_percentage)

# Create a summary dictionary
summary = {
    "Total Income": total_income,
    "Total Expenses": total_expense,
    "Balance": balance,
    "Savings Rate": savings_rate,
    "Expense Percentage": expense_percentage,
    "Total Transactions": total_transactions
}

print("\n--- Financial Summary ---")
print(summary)

# Convert summary dictionary into a DataFrame
summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["Metric", "Value"]
)

print("\n--- Summary DataFrame ---")
print(summary_df)

# Create a Month column
df["Month"] = df["Date"].dt.to_period("M")

print("\n--- Month Column ---")
print(df[["Date", "Month"]])

# Calculate monthly income
monthly_income = (
    df[df["Category"] == "Income"]
    .groupby("Month")["Amount"]
    .sum()
)

# Calculate monthly expenses
monthly_expenses = (
    df[df["Category"] != "Income"]
    .groupby("Month")["Amount"]
    .sum()
    .abs()
)

print("\n--- Monthly Income ---")
print(monthly_income)

print("\n--- Monthly Expenses ---")
print(monthly_expenses)

# Calculate monthly savings
monthly_savings = monthly_income - monthly_expenses

print("\n--- Monthly Savings ---")
print(monthly_savings)

# Create monthly financial summary
monthly_summary = pd.DataFrame({
    "Income": monthly_income,
    "Expenses": monthly_expenses,
    "Savings": monthly_savings
})

print("\n--- Monthly Financial Summary ---")
print(monthly_summary)

# Calculate monthly savings rate
monthly_summary["Savings Rate (%)"] = (
    monthly_summary["Savings"] / monthly_summary["Income"] * 100
)

print("\n--- Monthly Savings Rate ---")
print(monthly_summary[["Savings Rate (%)"]])

# Round savings rate to 2 decimal places
monthly_summary["Savings Rate (%)"] = (
    monthly_summary["Savings Rate (%)"].round(2)
)

print("\n--- Rounded Monthly Savings Rate ---")
print(monthly_summary[["Savings Rate (%)"]])

# Calculate monthly expense percentage
monthly_summary["Expense Percentage (%)"] = (
    monthly_summary["Expenses"] / monthly_summary["Income"] * 100
)

print("\n--- Monthly Expense Percentage ---")
print(monthly_summary[["Expense Percentage (%)"]])

# Round expense percentage to 2 decimal places
monthly_summary["Expense Percentage (%)"] = (
    monthly_summary["Expense Percentage (%)"].round(2)
)

print("\n--- Rounded Monthly Expense Percentage ---")
print(monthly_summary[["Expense Percentage (%)"]])

print("\n--- Complete Monthly Summary ---")
print(monthly_summary)

# Save monthly summary to CSV
monthly_summary.to_csv(
    "data/monthly_summary.csv",
    index=False
)

print("\nMonthly summary saved successfully!")

# Read the saved monthly summary
saved_summary = pd.read_csv(
    "data/monthly_summary.csv"
)

print("\n--- Saved Monthly Summary ---")
print(saved_summary)


# Create monthly income vs expenses chart
plt.figure(figsize=(10, 6))

plt.bar(
    monthly_summary.index.astype(str),
    monthly_summary["Income"],
    label="Income"
)

plt.bar(
    monthly_summary.index.astype(str),
    monthly_summary["Expenses"],
    label="Expenses"
)

plt.title("Monthly Income vs Expenses")
plt.xlabel("Month")
plt.ylabel("Amount (₹)")
plt.legend()

plt.tight_layout()

# Save chart as an image
plt.savefig("data/monthly_income_vs_expenses.png")

print("\nMonthly chart saved successfully!")

plt.show()

# Create expense by category chart
plt.figure(figsize=(10, 6))

expense_by_category.sort_values(ascending=False).plot(
    kind="bar"
)

plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Expense Amount (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/expense_by_category.png")

print("\nExpense by category chart saved successfully!")

plt.show()

# Create spending percentage chart
plt.figure(figsize=(10, 6))

category_percentage.sort_values(ascending=False).plot(
    kind="bar"
)

plt.title("Spending Percentage by Category")
plt.xlabel("Category")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/spending_percentage_by_category.png")

print("\nSpending percentage chart saved successfully!")

plt.show()

# Create monthly expense trend
monthly_expense_trend = monthly_summary["Expenses"]

print("\n--- Monthly Expense Trend ---")
print(monthly_expense_trend)

# Find the month with the highest expenses
highest_expense_month = monthly_expense_trend.idxmax()
highest_monthly_expense = monthly_expense_trend.max()

print("\n--- Highest Spending Month ---")
print("Month:", highest_expense_month)
print("Expense:", highest_monthly_expense)

# Calculate average monthly expense
average_monthly_expense = monthly_expense_trend.mean()

print("\n--- Average Monthly Expense ---")
print(average_monthly_expense)

# Calculate average monthly income
average_monthly_income = monthly_income.mean()

print("\n--- Average Monthly Income ---")
print(average_monthly_income)

# Calculate average monthly savings
average_monthly_savings = monthly_savings.mean()

print("\n--- Average Monthly Savings ---")
print(average_monthly_savings)

# Create average monthly metrics summary
average_monthly_summary = pd.DataFrame({
    "Metric": [
        "Average Monthly Income",
        "Average Monthly Expense",
        "Average Monthly Savings"
    ],
    "Amount": [
        average_monthly_income,
        average_monthly_expense,
        average_monthly_savings
    ]
})

print("\n--- Average Monthly Metrics ---")
print(average_monthly_summary)

# Save average monthly metrics to CSV
average_monthly_summary.to_csv(
    "data/average_monthly_summary.csv",
    index=False
)

print("\nAverage monthly summary saved successfully!")

# Read the saved average monthly summary
saved_average_summary = pd.read_csv(
    "data/average_monthly_summary.csv"
)

print("\n--- Saved Average Monthly Summary ---")
print(saved_average_summary)

# Get monthly savings percentage
monthly_savings_percentage = monthly_summary["Savings Rate (%)"]

print("\n--- Monthly Savings Percentage ---")
print(monthly_savings_percentage)

# Create monthly savings percentage chart
plt.figure(figsize=(10, 6))

monthly_savings_percentage.plot(
    kind="bar"
)

plt.title("Monthly Savings Rate")
plt.xlabel("Month")
plt.ylabel("Savings Rate (%)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_savings_rate.png")

print("\nMonthly savings rate chart saved successfully!")

plt.show()

# Calculate monthly balance
monthly_balance = monthly_income - monthly_expenses

print("\n--- Monthly Balance ---")
print(monthly_balance)

# Add monthly balance to the monthly summary
monthly_summary["Balance"] = monthly_balance

print("\n--- Monthly Summary with Balance ---")
print(monthly_summary)

# Save updated monthly summary
monthly_summary.to_csv(
    "data/monthly_summary.csv"
)

print("\nUpdated monthly summary saved successfully!")

# Read the updated monthly summary
updated_monthly_summary = pd.read_csv(
    "data/monthly_summary.csv"
)

print("\n--- Updated Monthly Summary from CSV ---")
print(updated_monthly_summary)

# Calculate monthly income-to-expense ratio
monthly_income_expense_ratio = (
    monthly_summary["Income"] / monthly_summary["Expenses"]
)

print("\n--- Monthly Income-to-Expense Ratio ---")
print(monthly_income_expense_ratio)

#Round the monthly income-to-expense ratio to 2 decimal places
monthly_income_expense_ratio_rounded = monthly_income_expense_ratio.round(2)

print("\n--- Rounded Monthly Income-to-Expense Ratio ---")
print(monthly_income_expense_ratio_rounded)

# Add income-to-expense ratio to monthly summary
monthly_summary["Income-to-Expense Ratio"] = (
    monthly_income_expense_ratio_rounded
)

print("\n--- Monthly Summary with Income-to-Expense Ratio ---")
print(monthly_summary)

# Save final monthly summary
monthly_summary.to_csv(
    "data/monthly_summary.csv"
)

print("\nFinal monthly summary saved successfully!")

# Create monthly balance chart
plt.figure(figsize=(10, 6))

monthly_balance.plot(
    kind="bar"
)

plt.title("Monthly Balance")
plt.xlabel("Month")
plt.ylabel("Balance (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_balance.png")

print("\nMonthly balance chart saved successfully!")

plt.show()

# Check total category spending percentage
total_category_percentage = category_percentage.sum()

print("\n--- Total Category Spending Percentage ---")
print(total_category_percentage)

#Round total category spending percentage to 2 decimal places
total_category_percentage_rounded = round(total_category_percentage, 2)

print("\n--- Rounded Total Category Spending Percentage ---")
print(total_category_percentage_rounded)

# Find the category with the lowest spending
lowest_expense_category = expense_by_category.idxmin()
lowest_expense_amount = expense_by_category.min()

print("\n--- Lowest Spending Category ---")
print("Category:", lowest_expense_category)
print("Amount:", lowest_expense_amount)

# Find the category with the largest expense percentage
largest_percentage_category = category_percentage_rounded.idxmax()
largest_percentage_value = category_percentage_rounded.max()

print("\n--- Largest Expense Percentage Category ---")
print("Category:", largest_percentage_category)
print("Percentage:", largest_percentage_value)

#Find the category with the smallest expense percentage
smallest_percentage_category = category_percentage_rounded.idxmin()
smallest_percentage_value = category_percentage_rounded.min()

print("\n--- Smallest Expense Percentage Category ---")
print("Category:", smallest_percentage_category)
print("Percentage:", smallest_percentage_value)

# Count expense transactions by category
expense_category_frequency = (
    df[df["Expense"] > 0]["Category"].value_counts()
)

print("\n--- Expense Category Frequency ---")
print(expense_category_frequency)

# Find the highest expense category frequency
highest_category_frequency = expense_category_frequency.max()

# Find all categories with the highest frequency
most_frequent_expense_categories = (
    expense_category_frequency[
        expense_category_frequency == highest_category_frequency
    ]
)

print("\n--- Most Frequent Expense Categories ---")
print(most_frequent_expense_categories)

# Calculate average expense by category
average_expense_by_category = (
    df[df["Expense"] > 0]
    .groupby("Category")["Expense"]
    .mean()
)

print("\n--- Average Expense by Category ---")
print(average_expense_by_category)

#Round average expense by category to 2 decimal places
average_expense_by_category_rounded = average_expense_by_category.round(2)  

print("\n--- Rounded Average Expense by Category ---")
print(average_expense_by_category_rounded)

# Find category with highest average expense
highest_average_expense_category = (
    average_expense_by_category_rounded.idxmax()
)

highest_average_expense_amount = (
    average_expense_by_category_rounded.max()
)

print("\n--- Highest Average Expense Category ---")
print("Category:", highest_average_expense_category)
print("Average Expense:", highest_average_expense_amount)

# Find category with lowest average expense
lowest_average_expense_category = (
    average_expense_by_category_rounded.idxmin()
)

lowest_average_expense_amount = (
    average_expense_by_category_rounded.min()
)

print("\n--- Lowest Average Expense Category ---")
print("Category:", lowest_average_expense_category)
print("Average Expense:", lowest_average_expense_amount)

# Calculate percentage of transactions that are expenses
expense_transaction_percentage = (
    expense_transactions / total_transactions
) * 100

print("\n--- Expense Transaction Percentage ---")
print(expense_transaction_percentage)

#Round expense transaction percentage to 2 decimal places
expense_transaction_percentage_rounded = round(expense_transaction_percentage, 2)

print("\n--- Rounded Expense Transaction Percentage ---")   
print(expense_transaction_percentage_rounded)

# Calculate percentage of transactions that are income
income_transaction_percentage = (
    income_transactions / total_transactions    
) * 100

print("\n--- Income Transaction Percentage ---")
print(income_transaction_percentage)

#Round income transaction percentage to 2 decimal places
income_transaction_percentage_rounded = round(income_transaction_percentage, 2)

print("\n--- Rounded Income Transaction Percentage ---")   
print(income_transaction_percentage_rounded)

# Validate transaction percentages
total_transaction_percentage = (
    income_transaction_percentage_rounded
    + expense_transaction_percentage_rounded
)

print("\n--- Total Transaction Percentage ---")
print(total_transaction_percentage)

# Create transaction type summary
transaction_type_summary = pd.DataFrame({
    "Transaction Type": [
        "Income",
        "Expense"
    ],
    "Count": [
        income_transactions,
        expense_transactions
    ],
    "Percentage": [
        income_transaction_percentage_rounded,
        expense_transaction_percentage_rounded
    ]
})

print("\n--- Transaction Type Summary ---")
print(transaction_type_summary)

# Save transaction type summary
transaction_type_summary.to_csv(
    "data/transaction_type_summary.csv",
    index=False
)

print("\nTransaction type summary saved successfully!")

# Read the saved transaction type summary
saved_transaction_summary = pd.read_csv(
    "data/transaction_type_summary.csv"
)

print("\n--- Saved Transaction Type Summary ---")
print(saved_transaction_summary)

# Create transaction distribution chart
plt.figure(figsize=(8, 5))

plt.bar(
    transaction_type_summary["Transaction Type"],
    transaction_type_summary["Count"]
)

plt.title("Transaction Distribution")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")

plt.tight_layout()

# Save chart
plt.savefig("data/transaction_distribution.png")

print("\nTransaction distribution chart saved successfully!")

plt.show()

# Create average expense by category chart
plt.figure(figsize=(10, 6))

average_expense_by_category_rounded.sort_values(
    ascending=False
).plot(
    kind="bar"
)

plt.title("Average Expense by Category")
plt.xlabel("Category")
plt.ylabel("Average Expense (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/average_expense_by_category.png")

print("\nAverage expense by category chart saved successfully!")

plt.show()

# Create income vs expense amount chart
plt.figure(figsize=(8, 5))

plt.bar(
    ["Income", "Expense"],
    [total_income, total_expense]
)

plt.title("Total Income vs Total Expenses")
plt.xlabel("Transaction Type")
plt.ylabel("Amount (₹)")

plt.tight_layout()

# Save chart
plt.savefig("data/income_vs_expense.png")

print("\nIncome vs expense chart saved successfully!")

plt.show()

# Create monthly savings chart
plt.figure(figsize=(10, 6))

monthly_summary["Savings"].plot(
    kind="bar"
)

plt.title("Monthly Savings")
plt.xlabel("Month")
plt.ylabel("Savings (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_savings.png")

print("\nMonthly savings chart saved successfully!")

plt.show()

# Create monthly expense trend chart
plt.figure(figsize=(10, 6))

monthly_summary["Expenses"].plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Expenses (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_expense_trend.png")

print("\nMonthly expense trend chart saved successfully!")

plt.show()

# Create monthly income trend chart
plt.figure(figsize=(10, 6))

monthly_summary["Income"].plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Income Trend")
plt.xlabel("Month")
plt.ylabel("Income (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_income_trend.png")

print("\nMonthly income trend chart saved successfully!")

plt.show()

# Create monthly savings rate chart
plt.figure(figsize=(10, 6))

monthly_summary["Savings Rate (%)"].plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Savings Rate")
plt.xlabel("Month")
plt.ylabel("Savings Rate (%)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_savings_rate.png")

print("\nMonthly savings rate chart saved successfully!")

plt.show()

# Create monthly balance chart
plt.figure(figsize=(10, 6))

monthly_summary["Balance"].plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Balance")
plt.xlabel("Month")
plt.ylabel("Balance (₹)")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_balance.png")

print("\nMonthly balance chart saved successfully!")

plt.show()

# Create monthly income vs expenses line chart
plt.figure(figsize=(10, 6))

monthly_summary["Income"].plot(
    kind="line",
    marker="o",
    label="Income"
)

monthly_summary["Expenses"].plot(
    kind="line",
    marker="o",
    label="Expenses"
)

plt.title("Monthly Income vs Expenses Trend")
plt.xlabel("Month")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_income_vs_expenses_trend.png")

print("\nMonthly income vs expenses trend chart saved successfully!")

plt.show()

# Create monthly income-to-expense ratio chart
plt.figure(figsize=(10, 6))

monthly_income_expense_ratio.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Income-to-Expense Ratio")
plt.xlabel("Month")
plt.ylabel("Income-to-Expense Ratio")
plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("data/monthly_income_expense_ratio.png")

print("\nMonthly income-to-expense ratio chart saved successfully!")

plt.show()

# Create financial KPI summary
financial_kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Income",
        "Total Expenses",
        "Balance",
        "Savings Rate (%)",
        "Expense Percentage (%)",
        "Total Transactions",
        "Income Transactions",
        "Expense Transactions",
        "Average Income",
        "Average Expense"
    ],
    "Value": [
        total_income,
        total_expense,
        balance,
        savings_rate_rounded,
        expense_percentage_rounded,
        total_transactions,
        income_transactions,
        expense_transactions,
        average_income,
        average_expense
    ]
})

print("\n--- Financial KPI Summary ---")
print(financial_kpi_summary)

#Round the values in the financial KPI summary to 2 decimal places
financial_kpi_summary["Value"] = financial_kpi_summary["Value"].round(2)

print("\n--- Rounded Financial KPI Summary ---")
print(financial_kpi_summary)

# Save financial KPI summary
financial_kpi_summary.to_csv(
    "data/financial_kpi_summary.csv",
    index=False
)

print("\nFinancial KPI summary saved successfully!")

# Read the saved financial KPI summary
saved_kpi_summary = pd.read_csv(
    "data/financial_kpi_summary.csv"
)

print("\n--- Saved Financial KPI Summary ---")
print(saved_kpi_summary)

# Create KPI cards data
kpi_cards = {
    "Total Income": total_income,
    "Total Expenses": total_expense,
    "Balance": balance,
    "Savings Rate": savings_rate_rounded,
    "Expense Percentage": expense_percentage_rounded
}

print("\n--- KPI Cards Data ---")
print(kpi_cards)

# Create dashboard-ready KPI DataFrame
kpi_cards_df = pd.DataFrame(
    list(kpi_cards.items()),
    columns=["Metric", "Value"]
)

print("\n--- Dashboard KPI DataFrame ---")
print(kpi_cards_df)

# Save dashboard KPI data
kpi_cards_df.to_csv(
    "data/kpi_cards.csv",
    index=False
)

print("\nDashboard KPI data saved successfully!")

# Read saved KPI cards
saved_kpi_cards = pd.read_csv(
    "data/kpi_cards.csv"
)

print("\n--- Saved KPI Cards ---")
print(saved_kpi_cards)

# Create dashboard data package
dashboard_data = {
    "transactions": df,
    "kpi_cards": kpi_cards_df,
    "category_spending": expense_by_category,
    "top_categories": top_3_categories,
    "monthly_summary": monthly_summary,
    "transaction_summary": transaction_type_summary
}

print("\n--- Dashboard Data Package ---")
print("Transactions:", dashboard_data["transactions"].shape)
print("KPI Cards:", dashboard_data["kpi_cards"].shape)
print("Category Spending:", dashboard_data["category_spending"].shape)
print("Top Categories:", dashboard_data["top_categories"].shape)
print("Monthly Summary:", dashboard_data["monthly_summary"].shape)
print("Transaction Summary:", dashboard_data["transaction_summary"].shape)

# Inspect dashboard data package
print("\n--- Dashboard Data Package Details ---")

for name, data in dashboard_data.items():
    print(f"\n{name}:")
    
    if isinstance(data, pd.DataFrame):
        print("Type: DataFrame")
        print("Shape:", data.shape)
        print("Columns:", list(data.columns))
    else:
        print("Type:", type(data).__name__)

# Create dashboard chart data
dashboard_charts = {
    "category_spending": expense_by_category,
    "top_categories": top_3_categories,
    "transaction_distribution": transaction_type_summary,
    "monthly_income": monthly_summary["Income"],
    "monthly_expenses": monthly_summary["Expenses"],
    "monthly_savings": monthly_summary["Savings"],
    "monthly_balance": monthly_summary["Balance"],
    "monthly_savings_rate": monthly_summary["Savings Rate (%)"],
    "monthly_expense_percentage": monthly_summary["Expense Percentage (%)"],
    "monthly_income_expense_ratio": monthly_summary["Income-to-Expense Ratio"]
}

print("\n--- Dashboard Chart Data ---")

for name, data in dashboard_charts.items():
    print(
        f"{name}: "
        f"{type(data).__name__}"
    )

# Create dashboard data summary
dashboard_summary = {
    "Total Transactions": len(df),
    "Total Categories": df["Category"].nunique(),
    "Total Months": df["Month"].nunique(),
    "Total Income": total_income,
    "Total Expenses": total_expense,
    "Total Savings": balance,
    "Top Spending Category": highest_expense_category,
    "Highest Spending Amount": highest_expense_amount
}

print("\n--- Dashboard Data Summary ---")

for key, value in dashboard_summary.items():
    print(f"{key}: {value}")