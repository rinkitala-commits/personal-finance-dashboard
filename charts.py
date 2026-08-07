import matplotlib.pyplot as plt


def expense_distribution_chart(expense_by_category):
    """
    Creates the expense distribution pie chart.
    """

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

    return fig

def top_spending_chart(expense_by_category):
    """
    Creates the Top Spending Categories chart.
    """

    fig, ax = plt.subplots(figsize=(8, 4))

    expense_by_category.sort_values().plot(
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

    return fig