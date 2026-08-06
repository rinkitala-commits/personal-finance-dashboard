import streamlit as st
import pandas as pd
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/transactions.csv")


# ============================================================
# DATA CLEANING
# ============================================================

# Clean category names
df["Category"] = df["Category"].replace("Billse", "Bills")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Create Income column
df["Income"] = df["Amount"].apply(
    lambda x: x if x > 0 else 0
)

# Create Expense column
df["Expense"] = df["Amount"].apply(
    lambda x: abs(x) if x < 0 else 0
)
# ============================================================
# FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

# Available categories
categories = ["All"] + sorted(
    df["Category"].unique().tolist()
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()


# ============================================================
# RESET FILTER CALLBACKS
# ============================================================

def reset_filters():
    st.session_state.selected_category = "All"
    st.session_state.selected_date_range = (
        min_date,
        max_date
    )


# ============================================================
# CATEGORY FILTER
# ============================================================

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories,
    key="selected_category"
)

# ============================================================
# DATE RANGE FILTER
# ============================================================

st.sidebar.subheader("📅 Date Filter")

selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="selected_date_range"
)
# ============================================================
# ACTIVE DATE RANGE
# ============================================================

if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_date, end_date = selected_date_range

    st.sidebar.caption(
        f"📅 Active period: "
        f"{start_date.strftime('%d %b %Y')} → "
        f"{end_date.strftime('%d %b %Y')}"
    )

# ============================================================
# ACTIVE CATEGORY
# ============================================================

if selected_category == "All":
    st.sidebar.caption("🛒 Active category: All categories")
else:
    st.sidebar.caption(
        f"🛒 Active category: {selected_category}"
    )

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# Apply category filter
if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ].copy()


# Apply date filter safely
if isinstance(selected_date_range, tuple):
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range

        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date)
            & (filtered_df["Date"].dt.date <= end_date)
        ].copy()

# ============================================================
# NO DATA CHECK
# ============================================================

if filtered_df.empty:
    st.warning(
        "⚠️ No transactions found for the selected filters."
    )
    st.stop()
# ============================================================
# SELECTED PERIOD
# ============================================================

if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_date, end_date = selected_date_range

    st.info(
        f"📅 Showing financial data from "
        f"{start_date.strftime('%d %b %Y')} "
        f"to "
        f"{end_date.strftime('%d %b %Y')}"
    )
# ============================================================
# ACTIVE TRANSACTION COUNT
# ============================================================
# ============================================================
# TRANSACTIONS IN VIEW
# ============================================================

st.sidebar.metric(
    "🧾 Transactions in View",
    len(filtered_df)
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv_data = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

# ============================================================
# DOWNLOAD COMPLETE TRANSACTION DATA
# ============================================================

all_transactions_csv = df.to_csv(index=False)

st.sidebar.download_button(
    label="⬇️ Download All Transactions",
    data=all_transactions_csv,
    file_name="all_transactions.csv",
    mime="text/csv"
)


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

total_income = filtered_df["Income"].sum()

total_expense = filtered_df["Expense"].sum()

balance = total_income - total_expense

savings_rate = (
    balance / total_income * 100
    if total_income > 0
    else 0
)

expense_percentage = (
    total_expense / total_income * 100
    if total_income > 0
    else 0
)
# ============================================================
# MONTHLY ANALYSIS
# ============================================================

filtered_df["Month"] = (
    filtered_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_income = (
    filtered_df.groupby("Month")["Income"]
    .sum()
)

monthly_expenses = (
    filtered_df.groupby("Month")["Expense"]
    .sum()
)

monthly_savings = (
    monthly_income - monthly_expenses
)

monthly_summary = pd.DataFrame({
    "Income": monthly_income,
    "Expenses": monthly_expenses,
    "Savings": monthly_savings
})

monthly_summary["Savings Rate (%)"] = (
    monthly_summary["Savings"]
    / monthly_summary["Income"]
    * 100
).fillna(0).round(2)

monthly_summary["Expense Percentage (%)"] = (
    monthly_summary["Expenses"]
    / monthly_summary["Income"]
    * 100
).fillna(0).round(2)


# ============================================================
# EXPENSE BY CATEGORY
# ============================================================

expense_by_category = (
    filtered_df[filtered_df["Expense"] > 0]
    .groupby("Category")["Expense"]
    .sum()
    .sort_values(ascending=False)
)
# ============================================================
# DOWNLOAD EXPENSE BY CATEGORY
# ============================================================

expense_by_category_csv = (
    expense_by_category
    .to_csv(header=["Expense"], index=True)
)

st.sidebar.download_button(
    label="⬇️ Download Expense by Category",
    data=expense_by_category_csv,
    file_name="expense_by_category.csv",
    mime="text/csv"
)


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("💰 Personal Finance Dashboard")

st.write(
    "Track your income, expenses, savings, and spending patterns."
)


# ============================================================
# FINANCIAL OVERVIEW
# ============================================================

st.header("📊 Financial Overview")
transaction_count = len(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Income",
    f"₹{total_income:,.2f}"
)

col2.metric(
    "💸 Total Expenses",
    f"₹{total_expense:,.2f}"
)

col3.metric(
    "💵 Balance",
    f"₹{balance:,.2f}"
)

col4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.2f}%"
)

col5.metric(
    "🧾 Transactions",
    transaction_count
)
# ============================================================
# EXPENSE PERCENTAGE
# ============================================================

st.metric(
    "📊 Expense Percentage",
    f"{expense_percentage:.2f}%"
)

# ============================================================
# TRANSACTION DATA
# ============================================================

# ============================================================
# TRANSACTION SEARCH
# ============================================================

def clear_transaction_search():
    st.session_state.transaction_search = ""


search_text = st.text_input(
    "🔎 Search transactions",
    placeholder="Search by description or category...",
    key="transaction_search"
)

st.button(
    "🧹 Clear Search",
    on_click=clear_transaction_search
)

if search_text:
    filtered_df = filtered_df[
        filtered_df["Description"].str.contains(
            search_text,
            case=False,
            na=False
        )
        |
        filtered_df["Category"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ].copy()
# ============================================================
# SEARCH STATUS
# ============================================================

if search_text:
    st.info(
        f"🔎 Showing transactions matching: **{search_text}**"
    )
# ============================================================
# TRANSACTION COUNT
# ============================================================

st.info(
    f"🧾 Transactions in view: {len(filtered_df)}"
)
# ============================================================
# TRANSACTION VIEW STATUS
# ============================================================

total_transactions = len(df)
visible_transactions = len(filtered_df)

st.caption(
    f"📋 Showing {visible_transactions} of "
    f"{total_transactions} transactions"
)

# Transaction table
st.header("🧾 Transactions")

transaction_display = filtered_df[
    [
        "Date",
        "Description",
        "Amount",
        "Category",
        "Income",
        "Expense"
    ]
].sort_values("Date").copy()

# Format date for display
transaction_display["Date"] = (
    transaction_display["Date"]
    .dt.strftime("%d %b %Y")
)

if filtered_df.empty:
    st.warning(
        "⚠️ No transactions found for the selected filters."
    )
else:
    st.dataframe(
        transaction_display.style.format({
            "Amount": "₹{:,.2f}",
            "Income": "₹{:,.2f}",
            "Expense": "₹{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# SAVINGS PROGRESS
# ============================================================

st.subheader("💰 Savings Progress")

savings_progress = min(max(savings_rate / 100, 0.0), 1.0)

st.progress(savings_progress)

st.write(
    f"You are saving {savings_rate:.2f}% of your income."
)

# ============================================================
# SAVINGS STATUS
# ============================================================

if savings_rate >= 50:
    st.success("🎉 Excellent! You are saving more than half of your income.")
elif savings_rate >= 20:
    st.info("👍 Good job! You have a healthy savings rate.")
elif savings_rate > 0:
    st.warning("⚠️ Your savings rate is low. Consider reviewing your expenses.")
else:
    st.error("🚨 You are currently not saving money.")

# ============================================================
# EXPENSE STATUS
# ============================================================

if expense_percentage <= 30:
    st.success("✅ Great! Your expenses are under 30% of your income.")
elif expense_percentage <= 50:
    st.info("👍 Your expenses are within 30%–50% of your income.")
elif expense_percentage <= 70:
    st.warning("⚠️ Your expenses are getting high. Review your spending.")
else:
    st.error("🚨 Your expenses are very high compared with your income.")

# ============================================================
# NET CASH FLOW STATUS
# ============================================================

if balance > 0:
    st.success(
        f"💵 Positive Net Cash Flow: ₹{balance:,.2f}"
    )
elif balance == 0:
    st.info(
        "⚖️ Your income and expenses are equal."
    )
else:
    st.error(
        f"🚨 Negative Net Cash Flow: ₹{abs(balance):,.2f}"
    )

# ============================================================
# SAVINGS AMOUNT STATUS
# ============================================================

if balance > 0:
    st.success(
        f"💰 You saved ₹{balance:,.2f} during the selected period."
    )
elif balance == 0:
    st.info(
        "⚖️ You have no savings during the selected period."
    )
else:
    st.error(
        f"⚠️ You spent ₹{abs(balance):,.2f} more than your income."
    )

# ============================================================
# FINANCIAL HEALTH SUMMARY
# ============================================================

st.header("❤️ Financial Health Summary")

if savings_rate >= 50 and expense_percentage <= 30 and balance > 0:
    st.success(
        "🟢 Excellent financial health! "
        "You have strong savings, controlled expenses, "
        "and positive cash flow."
    )

elif savings_rate >= 20 and expense_percentage <= 50 and balance > 0:
    st.info(
        "🟡 Good financial health. "
        "Your finances are positive, but there is room for improvement."
    )

elif balance > 0:
    st.warning(
        "🟠 Your finances are positive, "
        "but you should review your spending and savings."
    )

else:
    st.error(
        "🔴 Your financial position needs attention. "
        "Review your expenses and cash flow."
    )
# ============================================================
# FILTERED TRANSACTIONS
# ============================================================

st.header("📋 Filtered Transactions")
# ============================================================
# FILTERED TRANSACTION COUNT
# ============================================================

transaction_count = len(filtered_df)

st.metric(
    "🧾 Transactions",
    transaction_count
)

st.dataframe(
    filtered_df[
        ["Date", "Description", "Amount", "Category"]
    ],
    use_container_width=True
)

# ============================================================
# DOWNLOAD FILTERED TRANSACTIONS
# ============================================================

filtered_csv = filtered_df[
    ["Date", "Description", "Amount", "Category"]
].to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Transactions",
    data=filtered_csv,
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

# ============================================================
# SPENDING BY CATEGORY
# ============================================================

st.header("🛒 Spending by Category")

st.bar_chart(
    expense_by_category
)

# ============================================================
# EXPENSE DISTRIBUTION
# ============================================================

import matplotlib.pyplot as plt

st.header("🥧 Expense Distribution")

fig, ax = plt.subplots(figsize=(7, 7))

explode = [0.08] + [0] * (len(expense_by_category) - 1)

wedges, texts, autotexts = ax.pie(
    expense_by_category,
    autopct="%1.1f%%",
    startangle=90,
    explode=explode
)

ax.legend(
    wedges,
    expense_by_category.index,
    title="Categories",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

ax.set_ylabel("")
ax.set_title("Expense Distribution by Category")

st.pyplot(fig)

st.success(
    f"💸 Total Spending: ₹{expense_by_category.sum():,.2f}"
)

# ============================================================
# AVERAGE DAILY EXPENSE
# ============================================================

days = filtered_df["Date"].dt.date.nunique()

if days > 0:
    average_daily_expense = total_expense / days

    st.info(
        f"📅 Average Daily Expense: ₹{average_daily_expense:,.2f}"
    )

# ============================================================
# HIGHEST SINGLE EXPENSE
# ============================================================

highest_expense = filtered_df["Expense"].max()

st.info(
    f"💳 Highest Single Expense: ₹{highest_expense:,.2f}"
)

# ============================================================
# LOWEST SINGLE EXPENSE
# ============================================================

expense_transactions = filtered_df[
    filtered_df["Expense"] > 0
]

if not expense_transactions.empty:
    lowest_expense = expense_transactions["Expense"].min()

    st.info(
        f"🪙 Lowest Single Expense: ₹{lowest_expense:,.2f}"
    )

# ============================================================
# HIGHEST INCOME
# ============================================================

income_transactions = filtered_df[
    filtered_df["Income"] > 0
]

if not income_transactions.empty:
    highest_income = income_transactions["Income"].max()

    st.info(
        f"💰 Highest Income: ₹{highest_income:,.2f}"
    )

# ============================================================
# LOWEST INCOME
# ============================================================

if not income_transactions.empty:
    lowest_income = income_transactions["Income"].min()

    st.info(
        f"💵 Lowest Income: ₹{lowest_income:,.2f}"
    )

# ============================================================
# AVERAGE TRANSACTION AMOUNT
# ============================================================

average_transaction = filtered_df["Amount"].mean()

st.info(
    f"🧮 Average Transaction Amount: ₹{average_transaction:,.2f}"
)

# ============================================================
# EXPENSE TO INCOME RATIO
# ============================================================

if total_income > 0:
    expense_income_ratio = (total_expense / total_income) * 100

    st.info(
        f"⚖️ Expense to Income Ratio: {expense_income_ratio:.2f}%"
    )

# ============================================================
# INCOME VS EXPENSE PROGRESS
# ============================================================

st.subheader("📊 Income vs Expense")

if total_income > 0:
    income_progress = 1.0
    expense_progress = total_expense / total_income

    st.write("💰 Income")
    st.progress(income_progress)

    st.write("💸 Expenses")
    st.progress(min(expense_progress, 1.0))
# ============================================================
# TOP SPENDING CATEGORIES
# ============================================================

st.header("🏆 Top Spending Categories")

fig, ax = plt.subplots(figsize=(8, 4))

bars = expense_by_category.sort_values().plot(
    kind="barh",
    ax=ax
)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="₹%.0f",
        padding=5
    )

ax.set_xlabel("Amount (₹)")
ax.set_ylabel("Category")
ax.set_title("Top Spending Categories")

st.pyplot(fig)

# ============================================================
# MONTHLY FINANCIAL SUMMARY
# ============================================================

st.header("📅 Monthly Financial Summary")

monthly_summary_display = monthly_summary.copy()

monthly_summary_display["Transactions"] = (
    filtered_df.groupby("Month")
    .size()
)

monthly_summary_display["Transactions"] = (
    monthly_summary_display["Transactions"]
    .fillna(0)
    .astype(int)
)

st.dataframe(
    monthly_summary_display,
    use_container_width=True
)

# ============================================================
# DOWNLOAD MONTHLY SUMMARY
# ============================================================

monthly_summary_csv = monthly_summary.to_csv(index=True)

st.download_button(
    label="⬇️ Download Monthly Summary",
    data=monthly_summary_csv,
    file_name="monthly_financial_summary.csv",
    mime="text/csv"
)
# ============================================================
# MONTHLY INCOME VS EXPENSES
# ============================================================

st.header("📈 Monthly Income vs Expenses")

monthly_income_expense_chart = monthly_summary[
    ["Income", "Expenses"]
]

st.bar_chart(
    monthly_income_expense_chart,
    stack=False
)


# ============================================================
# MONTHLY SAVINGS
# ============================================================

st.header("💵 Monthly Savings")

monthly_savings_chart = monthly_summary[
    ["Savings"]
]

st.line_chart(
    monthly_savings_chart
)

# ============================================================
# MONTHLY SAVINGS RATE
# ============================================================

st.header("📊 Monthly Savings Rate")

monthly_savings_rate_chart = monthly_summary[
    ["Savings Rate (%)"]
]

st.line_chart(
    monthly_savings_rate_chart
)

# ============================================================
# MONTHLY EXPENSE PERCENTAGE
# ============================================================

st.header("📉 Monthly Expense Percentage")

monthly_expense_percentage_chart = monthly_summary[
    ["Expense Percentage (%)"]
]

st.line_chart(
    monthly_expense_percentage_chart
)

# ============================================================
# CATEGORY SPENDING PERCENTAGE
# ============================================================

st.header("📊 Spending Percentage by Category")

category_percentage_chart = (
    filtered_df[filtered_df["Expense"] > 0]
    .groupby("Category")["Expense"]
    .sum()
)

category_percentage_chart = (
    category_percentage_chart
    / total_expense
    * 100
)

category_percentage_chart = (
    category_percentage_chart
    .sort_values(ascending=False)
    .round(2)
)

st.bar_chart(
    category_percentage_chart
)
# ============================================================
# DOWNLOAD CATEGORY SPENDING PERCENTAGE
# ============================================================

category_percentage_csv = (
    category_percentage_chart
    .to_csv(header=["Percentage"], index=True)
)

st.sidebar.download_button(
    label="⬇️ Download Category Percentage",
    data=category_percentage_csv,
    file_name="category_spending_percentage.csv",
    mime="text/csv"
)

# ============================================================
# TOP 3 SPENDING CATEGORIES
# ============================================================

st.header("🏆 Top 3 Spending Categories")

top_col1, top_col2, top_col3 = st.columns(3)

top_categories = expense_by_category.head(3)

for col, (category, amount) in zip(
    [top_col1, top_col2, top_col3],
    top_categories.items()
):
    col.metric(
        category,
        f"₹{amount:,.2f}"
    )

# ============================================================
# DOWNLOAD TOP 3 SPENDING CATEGORIES
# ============================================================

top_categories_csv = (
    top_categories
    .to_csv(header=["Expense"], index=True)
)

st.sidebar.download_button(
    label="⬇️ Download Top 3 Categories",
    data=top_categories_csv,
    file_name="top_3_spending_categories.csv",
    mime="text/csv"
)

# ============================================================
# COMPLETE FINANCIAL SUMMARY DOWNLOAD
# ============================================================

financial_summary = pd.DataFrame({
    "Metric": [
        "Total Income",
        "Total Expenses",
        "Balance",
        "Savings Rate (%)",
        "Expense Percentage (%)",
        "Transactions"
    ],
    "Value": [
        total_income,
        total_expense,
        balance,
        round(savings_rate, 2),
        round(expense_percentage, 2),
        len(filtered_df)
    ]
})

financial_summary_csv = financial_summary.to_csv(index=False)

st.sidebar.download_button(
    label="⬇️ Download Financial Summary",
    data=financial_summary_csv,
    file_name="financial_summary.csv",
    mime="text/csv"
)

# ============================================================
# RESET BUTTON
# ============================================================

st.sidebar.button(
    "🔄 Reset Filters",
    on_click=reset_filters
)

# ============================================================
# DASHBOARD FOOTER
# ============================================================

st.divider()

st.caption(
    "💰 Personal Finance Dashboard • "
    "Built with Python, Pandas, and Streamlit"
)

# ============================================================
# LAST UPDATED
# ============================================================

st.caption(
    f"🕒 Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
)