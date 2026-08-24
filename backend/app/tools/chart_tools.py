import pandas as pd


def create_bar_chart(
    df: pd.DataFrame,
    category_column: str,
    value_column: str,
    aggregation: str = "sum"
) -> dict:

    if category_column not in df.columns:
        raise ValueError(
            f"Column '{category_column}' does not exist."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        raise ValueError(
            f"Column '{value_column}' must be numeric."
        )

    if aggregation == "sum":

        grouped = (
            df.groupby(category_column)[value_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        grouped = (
            df.groupby(category_column)[value_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        grouped = (
            df.groupby(category_column)[value_column]
            .count()
            .reset_index()
        )

    else:

        raise ValueError(
            "Aggregation must be sum, mean, or count."
        )

    return {
        "chart_type": "bar",
        "title": (
            f"{aggregation.title()} of "
            f"{value_column} by "
            f"{category_column}"
        ),
        "x_axis": category_column,
        "y_axis": value_column,
        "aggregation": aggregation,
        "data": grouped.to_dict(
            orient="records"
        )
    }

def create_line_chart(
    df: pd.DataFrame,
    x_column: str,
    value_column: str,
    aggregation: str = "sum"
) -> dict:

    if x_column not in df.columns:
        raise ValueError(
            f"Column '{x_column}' does not exist."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        raise ValueError(
            f"Column '{value_column}' must be numeric."
        )

    if aggregation == "sum":

        grouped = (
            df.groupby(x_column)[value_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        grouped = (
            df.groupby(x_column)[value_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        grouped = (
            df.groupby(x_column)[value_column]
            .count()
            .reset_index()
        )

    else:

        raise ValueError(
            "Aggregation must be sum, mean, or count."
        )

    # Preserve chronological order for month names
    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    if x_column in df.columns:

        values = (
            grouped[x_column]
            .astype(str)
            .str.strip()
        )

        normalized_values = values.str[:3].str.title()

        if normalized_values.isin(month_order).all():

            grouped[x_column] = pd.Categorical(
                normalized_values,
                categories=month_order,
                ordered=True
            )

            grouped = grouped.sort_values(
                x_column
            )

            grouped[x_column] = (
                grouped[x_column]
                .astype(str)
            )

        else:

            original_order = (
                df[x_column]
                .drop_duplicates()
                .astype(str)
                .tolist()
            )

            grouped[x_column] = pd.Categorical(
                values,
                categories=original_order,
                ordered=True
            )

            grouped = grouped.sort_values(
                x_column
            )

            grouped[x_column] = (
                grouped[x_column]
                .astype(str)
            )

    return {
        "chart_type": "line",
        "title": (
            f"{aggregation.title()} of "
            f"{value_column} by "
            f"{x_column}"
        ),
        "x_axis": x_column,
        "y_axis": value_column,
        "aggregation": aggregation,
        "data": grouped.to_dict(
            orient="records"
        )
    }


def create_pie_chart(
    df: pd.DataFrame,
    category_column: str,
    value_column: str,
    aggregation: str = "sum"
) -> dict:

    if category_column not in df.columns:
        raise ValueError(
            f"Column '{category_column}' does not exist."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        raise ValueError(
            f"Column '{value_column}' must be numeric."
        )

    if aggregation == "sum":

        grouped = (
            df.groupby(category_column)[value_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        grouped = (
            df.groupby(category_column)[value_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        grouped = (
            df.groupby(category_column)[value_column]
            .count()
            .reset_index()
        )

    else:

        raise ValueError(
            "Aggregation must be sum, mean, or count."
        )

    return {
        "chart_type": "pie",
        "title": (
            f"{aggregation.title()} of "
            f"{value_column} by "
            f"{category_column}"
        ),
        "category_column": category_column,
        "value_column": value_column,
        "aggregation": aggregation,
        "data": grouped.to_dict(
            orient="records"
        )
    }


def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str
) -> dict:

    if x_column not in df.columns:
        raise ValueError(
            f"Column '{x_column}' does not exist."
        )

    if y_column not in df.columns:
        raise ValueError(
            f"Column '{y_column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[x_column]
    ):
        raise ValueError(
            f"Column '{x_column}' must be numeric."
        )

    if not pd.api.types.is_numeric_dtype(
        df[y_column]
    ):
        raise ValueError(
            f"Column '{y_column}' must be numeric."
        )

    data = df[
        [x_column, y_column]
    ].dropna()

    return {
        "chart_type": "scatter",
        "title": (
            f"{y_column} vs {x_column}"
        ),
        "x_axis": x_column,
        "y_axis": y_column,
        "data": data.to_dict(
            orient="records"
        )
    }