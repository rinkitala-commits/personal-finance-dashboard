import pandas as pd


def apply_filters(
    df,
    selected_category,
    selected_date_range
):
    """
    Apply dashboard filters.
    """

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ].copy()

    if (
        isinstance(selected_date_range, tuple)
        and len(selected_date_range) == 2
    ):
        start_date, end_date = selected_date_range

        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date)
            &
            (filtered_df["Date"].dt.date <= end_date)
        ].copy()

    return filtered_df