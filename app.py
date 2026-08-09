import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import analytics
import charts
from data_manager import load_transactions
import filters
import downloads
from database.database_manager import (
    create_transactions_table,
    load_transactions_from_database,
    add_transaction,
    delete_transaction
)

create_transactions_table()

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

df = load_transactions_from_database()

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
st.sidebar.divider()
st.sidebar.header("🔎 Filters")


# Available categories
categories = ["All"] + sorted(
    df["Category"].unique().tolist()
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

# ============================================================
# RESET FILTER CALLBACK
# ============================================================

def reset_filters():
    st.session_state.selected_category = "All"
    st.session_state.selected_date_range = (
        min_date,
        max_date
    )


# ============================================================
# RESET BUTTON
# ============================================================

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):
    st.session_state.selected_category = "All"
    st.session_state.selected_date_range = (
        min_date,
        max_date
    )
    st.rerun()

# ============================================================
# CATEGORY FILTER
# ============================================================

selected_category = st.sidebar.selectbox(
    "🏷️ Category",
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
# ACTIVE FILTER STATUS
# ============================================================

if (
    isinstance(selected_date_range, tuple)
    and len(selected_date_range) == 2
):

    start_date, end_date = selected_date_range

    st.sidebar.caption(
        f"📅 Active period: "
        f"{start_date.strftime('%d %b %Y')} → "
        f"{end_date.strftime('%d %b %Y')}"
    )


if selected_category == "All":

    st.sidebar.caption(
        "🛒 Active category: All categories"
    )

else:

    st.sidebar.caption(
        f"🛒 Active category: {selected_category}"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = filters.apply_filters(
    df,
    selected_category,
    selected_date_range
)


# ============================================================
# NO DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No transactions found for the selected filters."
    )

    st.stop()

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
# ADD TRANSACTION
# ============================================================
st.sidebar.divider()
st.sidebar.header("➕ Add Transaction")
st.sidebar.caption(
    "Add a new income or expense transaction."
)

with st.sidebar.form("add_transaction_form"):

    transaction_date = st.date_input(
        "Date",
        help="Select the date of this transaction."
    )

    transaction_description = st.text_input(
    "Description",
    placeholder="e.g. Grocery shopping, Salary, Electricity bill"
    )

    transaction_amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=100.0
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"],
        help="Choose whether this transaction is money you spent or money you received."
    )

    transaction_category = st.selectbox(
        "Category",
        [
            "Food",
            "Shopping",
            "Bills",
            "Transport",
            "Entertainment",
            "Education",
            "Health",
            "Salary",
            "Other"
        ]
    )

    submit_transaction = st.form_submit_button(
        "➕ Add Transaction"
    )


if submit_transaction:

    if not transaction_description.strip():

        st.sidebar.error(
            "Please enter a description."
        )

    elif not transaction_category.strip():

        st.sidebar.error(
            "Please enter a category."
        )

    elif transaction_amount <= 0:

        st.sidebar.error(
            "Amount must be greater than ₹0."
        )

    else:

        if transaction_type == "Expense":
            database_amount = -transaction_amount
        else:
            database_amount = transaction_amount

        add_transaction(
            transaction_date.strftime("%Y-%m-%d"),
            transaction_description,
            database_amount,
            transaction_category
        )

        st.sidebar.success(
            "✅ Transaction added successfully!"
        )

        st.rerun()

# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

income = analytics.total_income(filtered_df)
expense = analytics.total_expense(filtered_df)
current_balance = analytics.balance(filtered_df)
current_savings_rate = analytics.savings_rate(filtered_df)
current_expense_percentage = analytics.expense_percentage(filtered_df)
expense_by_category = analytics.expense_by_category(filtered_df)



# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("💰 Personal Finance Dashboard")

st.write(
    "Track your income, expenses, savings, and spending patterns."
)
st.divider()
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
# MONTHLY ANALYSIS
# ============================================================

monthly_summary = analytics.monthly_summary(filtered_df)

# ============================================================
# FINANCIAL OVERVIEW
# ============================================================

st.header("📊 Financial Overview")

st.caption(
    "A quick overview of your income, expenses, balance, savings, and transactions."
)

transaction_count = len(filtered_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Income",
        f"₹{income:,.2f}"
    )

with col2:
    st.metric(
        "💸 Total Expenses",
        f"₹{expense:,.2f}"
    )

with col3:
    st.metric(
        "💵 Balance",
        f"₹{current_balance:,.2f}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "📈 Savings Rate",
        f"{current_savings_rate:.2f}%"
    )

with col5:
    st.metric(
        "📊 Expense Percentage",
        f"{current_expense_percentage:.2f}%"
    )

with col6:
    st.metric(
        "🧾 Transactions",
        transaction_count
    )

st.divider()
# ============================================================
# INCOME VS EXPENSE
# ============================================================

st.subheader("📊 Income vs Expense")

st.caption(
    "Compare your total income with your spending for the selected period."
)

income_col, expense_col = st.columns(2)

with income_col:
    st.metric(
        "💰 Income",
        f"₹{income:,.2f}"
    )

with expense_col:
    st.metric(
        "💸 Expenses",
        f"₹{expense:,.2f}"
    )

if income > 0:
    expense_ratio = (expense / income) * 100

    st.caption(
        f"💡 You spent {expense_ratio:.2f}% of your income."
    )

    st.progress(
        min(expense_ratio / 100, 1.0)
    )
else:
    st.info("No income available for comparison.")

st.divider()

# ============================================================
# EXPENSE BY CATEGORY
# ============================================================

st.header("📊 Expense by Category")

st.caption(
    "See how your expenses are distributed across different categories."
)

if expense_by_category.empty:

    st.info("No expense data available for the selected filters.")

else:

    fig = charts.expense_distribution_chart(
        expense_by_category
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.caption(
        "💡 This chart shows how your total expenses are distributed across categories."
    )
st.divider()
# ============================================================
# TOP SPENDING CATEGORIES
# ============================================================

st.header("🏆 Top Spending Categories")

st.caption(
    "Your highest spending categories for the selected period."
)

if expense_by_category.empty:

    st.info("No spending data available for the selected filters.")

else:

    fig = charts.top_spending_chart(
        expense_by_category
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.caption(
        "💡 Categories are ranked by total spending, from highest to lowest."
    )
st.divider()

# ============================================================
# TRANSACTION STATISTICS
# ============================================================

st.header("📈 Transaction Statistics")

st.caption(
    "Detailed statistics for the transactions in the selected period."
)

statistics = analytics.transaction_statistics(
    filtered_df,
    income,
    expense
)

st.metric(
    "💸 Total Spending",
    f"₹{expense_by_category.sum():,.2f}"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📅 Average Daily Expense",
        f"₹{statistics['average_daily_expense']:,.2f}"
    )

with col2:
    st.metric(
        "💳 Highest Single Expense",
        f"₹{statistics['highest_expense']:,.2f}"
    )

with col3:
    st.metric(
        "🪙 Lowest Single Expense",
        f"₹{statistics['lowest_expense']:,.2f}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "💰 Highest Income",
        f"₹{statistics['highest_income']:,.2f}"
    )

with col5:
    st.metric(
        "💵 Lowest Income",
        f"₹{statistics['lowest_income']:,.2f}"
    )

with col6:
    st.metric(
        "🧮 Average Transaction",
        f"₹{statistics['average_transaction']:,.2f}"
    )


st.metric(
    "⚖️ Expense to Income Ratio",
    f"{statistics['expense_income_ratio']:.2f}%"
)
st.divider()

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

# ============================================================
# FILTERED TRANSACTIONS
# ============================================================

st.header("🧾 Filtered Transactions")

st.caption(
    "Transactions matching your current filters."
)

if filtered_df.empty:

    st.info(
        "⚠️ No transactions found for the selected filters."
    )

else:

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
    # ========================================================
    # DOWNLOAD FILTERED TRANSACTIONS
    # ========================================================

    filtered_csv = filtered_df[
        ["Date", "Description", "Amount", "Category"]
    ].to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered Transactions",
        data=filtered_csv,
        file_name="filtered_transactions.csv",
        mime="text/csv"
    )

    # ========================================================
    # FORMAT DATE
    # ========================================================

    transaction_display["Date"] = (
        transaction_display["Date"]
        .dt.strftime("%d %b %Y")
    )

    # ========================================================
    # DISPLAY TABLE
    # ========================================================

    display_df = transaction_display.copy()

    st.dataframe(
        display_df.style.format({
            "Amount": "₹{:,.2f}",
            "Income": "₹{:,.2f}",
            "Expense": "₹{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"🧾 Showing {visible_transactions} transaction(s) "
        "matching the selected filters."
    )

st.divider()
# ============================================================
# DELETE TRANSACTION
# ============================================================
st.sidebar.divider()
st.sidebar.subheader("🗑️ Delete Transaction")
st.sidebar.caption(
    "Select a transaction below if you want to remove it."
)

if not filtered_df.empty:

    delete_options = filtered_df[
        [
            "transaction_id",
            "Date",
            "Description",
            "Amount",
            "Category"
        ]
    ].copy()

    delete_options["Display"] = (
        delete_options["Date"].dt.strftime("%d %b %Y")
        + " | "
        + delete_options["Description"]
        + " | ₹"
        + delete_options["Amount"].abs().map(
            lambda x: f"{x:,.2f}"
        )
        + " | "
        + delete_options["Category"]
    )

    selected_transaction = st.sidebar.selectbox(
        "Select transaction to delete",
        delete_options["Display"].tolist(),
        key="delete_transaction_select"
    )

    delete_button = st.sidebar.button(
        "🗑️ Delete Selected Transaction",
        key="delete_transaction_button",
        type = "secondary"
    )

    if delete_button:

        selected_row = delete_options[
            delete_options["Display"] == selected_transaction
        ].iloc[0]

        transaction_id = int(
            selected_row["transaction_id"]
        )

        delete_transaction(transaction_id)

        st.sidebar.success(
            "✅ Transaction deleted successfully!"
        )

        st.rerun()

else:

    st.sidebar.info(
        "No transactions available to delete."
    )
# ============================================================
# DOWNLOADS
# ============================================================
st.sidebar.divider()
st.sidebar.header("📥 Downloads")


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
# SAVINGS PROGRESS
# ============================================================

st.subheader("💰 Savings Progress")

st.caption(
    "Track how much of your income you are currently saving."
)

if income > 0:

    savings_progress = min(
        max(current_savings_rate / 100, 0.0),
        1.0
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            "💰 Savings Rate",
            f"{current_savings_rate:.2f}%"
        )

    with col2:
        st.write("📈 Savings Progress")
        st.progress(savings_progress)

    st.caption(
        f"You are currently saving {current_savings_rate:.2f}% "
        "of your income."
    )

else:

    st.info(
        "ℹ️ No income available to calculate your savings rate."
    )
st.divider()
# ============================================================
# SAVINGS STATUS
# ============================================================

st.subheader("🎯 Savings Status")

if income <= 0:

    st.info(
        "ℹ️ Add income to see your savings status."
    )

elif current_savings_rate >= 50:

    st.success(
        "🎉 Excellent! You are saving more than half of your income."
    )

elif current_savings_rate >= 20:

    st.info(
        "👍 Good job! You have a healthy savings rate."
    )

elif current_savings_rate > 0:

    st.warning(
        "⚠️ Your savings rate is low. Consider reviewing your expenses."
    )

else:

    st.error(
        "🚨 You are currently not saving money."
    )

st.divider()
# ============================================================
# NET CASH FLOW STATUS
# ============================================================

if current_balance > 0:
    st.success(
        f"💵 Positive Net Cash Flow: ₹{current_balance:,.2f}"
    )
elif current_balance == 0:
    st.info(
        "⚖️ Your income and expenses are equal."
    )
else:
    st.error(
        f"🚨 Negative Net Cash Flow: ₹{abs(current_balance):,.2f}"
    )

# ============================================================
# SAVINGS AMOUNT STATUS
# ============================================================

if current_balance > 0:
    st.success(
        f"💰 You saved ₹{current_balance:,.2f} during the selected period."
    )
elif current_balance == 0:
    st.info(
        "⚖️ You have no savings during the selected period."
    )
else:
    st.error(
        f"⚠️ You spent ₹{abs(current_balance):,.2f} more than your income."
    )
st.divider()
# ============================================================
# FINANCIAL HEALTH SUMMARY
# ============================================================

st.header("❤️ Financial Health Summary")

if current_savings_rate >= 50 and current_expense_percentage <= 30 and current_balance > 0:
    st.success(
        "🟢 Excellent financial health! "
        "You have strong savings, controlled expenses, "
        "and positive cash flow."
    )

elif current_savings_rate >= 20 and current_expense_percentage <= 50 and current_balance > 0:
    st.info(
        "🟡 Good financial health. "
        "Your finances are positive, but there is room for improvement."
    )

elif current_balance > 0:
    st.warning(
        "🟠 Your finances are positive, "
        "but you should review your spending and savings."
    )

else:
    st.error(
        "🔴 Your financial position needs attention. "
        "Review your expenses and cash flow."
    )
st.divider()
# ============================================================
# SPENDING BY CATEGORY
# ============================================================

st.subheader("🛒 Spending by Category")

st.bar_chart(
    expense_by_category
)

st.caption(
    "💡 Compare your spending across different categories."
)

st.divider()
# ============================================================
# DOWNLOAD EXPENSE BY CATEGORY
# ============================================================

expense_by_category_csv = expense_by_category.to_frame(
    name="Expense"
).to_csv(index=True)

st.sidebar.download_button(
    label="⬇️ Download Expense by Category",
    data=expense_by_category_csv,
    file_name="expense_by_category.csv",
    mime="text/csv"
)

# ============================================================
# MONTHLY FINANCIAL SUMMARY
# ============================================================

st.header("📅 Monthly Financial Summary")

st.caption(
    "Review your income, expenses, savings, and financial ratios month by month."
)

monthly_summary_display = monthly_summary.copy()

st.dataframe(
    monthly_summary_display,
    use_container_width=True,
    hide_index=False
)

st.caption(
    "📅 Monthly overview of income, expenses, savings, "
    "and financial ratios."
)
st.divider()
# ============================================================
# DOWNLOAD MONTHLY SUMMARY
# ============================================================

monthly_summary_csv = monthly_summary.to_csv(index=True)

st.sidebar.download_button(
    label="⬇️ Download Monthly Summary",
    data=monthly_summary_csv,
    file_name="monthly_financial_summary.csv",
    mime="text/csv"
)
# ============================================================
# MONTHLY INCOME VS EXPENSES
# ============================================================

st.subheader("📈 Monthly Income vs Expenses")

monthly_income_expense_chart = monthly_summary[
    ["Income", "Expenses"]
]

st.bar_chart(
    monthly_income_expense_chart,
    stack=False
)

st.caption(
    "💡 Compare your monthly income with your monthly expenses."
)
st.divider()

# ============================================================
# MONTHLY SAVINGS
# ============================================================

st.subheader("💵 Monthly Savings")

monthly_savings_chart = monthly_summary[
    ["Savings"]
]

st.line_chart(
    monthly_savings_chart
)

st.caption(
    "💡 Track how your monthly savings change over time."
)
st.divider()
# ============================================================
# MONTHLY SAVINGS RATE
# ============================================================

st.subheader("📊 Monthly Savings Rate")

monthly_savings_rate_chart = monthly_summary[
    ["Savings Rate (%)"]
]

st.line_chart(
    monthly_savings_rate_chart
)

st.caption(
    "💡 Track the percentage of income saved each month."
)
st.divider()

# ============================================================
# MONTHLY EXPENSE PERCENTAGE
# ============================================================

st.subheader("📉 Monthly Expense Percentage")

monthly_expense_percentage_chart = monthly_summary[
    ["Expense Percentage (%)"]
]

st.line_chart(
    monthly_expense_percentage_chart
)

st.caption(
    "💡 Track the percentage of income spent each month."
)
st.divider()
# ============================================================
# CATEGORY SPENDING PERCENTAGE
# ============================================================

st.subheader("📊 Spending Percentage by Category")

st.caption(
    "Compare how much of your total spending comes from each category."
)

if expense > 0:

    category_percentage_chart = (
        filtered_df[filtered_df["Expense"] > 0]
        .groupby("Category")["Expense"]
        .sum()
    )

    category_percentage_chart = (
        category_percentage_chart
        / expense
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

    st.caption(
        "💡 Compare the percentage of total spending across categories."
    )

else:

    st.info(
        "No expense data available for the selected filters."
    )

st.divider()
# ============================================================
# DOWNLOAD CATEGORY SPENDING PERCENTAGE
# ============================================================

if expense > 0:

    category_percentage_csv = (
        category_percentage_chart
        .to_csv(
            header=["Percentage"],
            index=True
        )
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

st.subheader("🏆 Top 3 Spending Categories")

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
    income,
        expense,
        current_balance,
        round(current_savings_rate, 2),
        round(current_expense_percentage, 2),
        len(filtered_df)
    ]
})

financial_summary_csv = financial_summary.to_csv(index=False)

st.sidebar.download_button(
    label="⬇️ Complete Financial Summary",
    data=financial_summary_csv,
    file_name="financial_summary.csv",
    mime="text/csv"
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
