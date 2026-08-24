import pandas as pd


def get_dataset_summary(df: pd.DataFrame) -> dict:

    numerical_columns = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    month_names = {
    "jan", "january",
    "feb", "february",
    "mar", "march",
    "apr", "april",
    "may",
    "jun", "june",
    "jul", "july",
    "aug", "august",
    "sep", "sept", "september",
    "oct", "october",
    "nov", "november",
    "dec", "december"
}

    month_columns = []

    date_columns = []

    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            date_columns.append(column)

        elif pd.api.types.is_string_dtype(
            df[column]
        ):

            values = (
                df[column]
                .dropna()
                .astype(str)
                .str.strip()
                .str.lower()
            )

            # Detect month-name columns separately.
            if (
                not values.empty
                and values.isin(month_names).all()
            ):
                month_columns.append(column)
                continue

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                date_columns.append(column)

    categorical_columns = (
        df.select_dtypes(
            include=["object", "category", "string"]
        )
        .columns
        .tolist()
    )

    categorical_columns = [
        column
        for column in categorical_columns
        if column not in date_columns
        and column not in month_columns
    ]

    date_ranges = {}

    for column in date_columns:

        converted_dates = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_dates = converted_dates.dropna()

        if not valid_dates.empty:
            date_ranges[column] = {
                "min": valid_dates.min().strftime(
                    "%Y-%m-%d"
                ),
                "max": valid_dates.max().strftime(
                    "%Y-%m-%d"
                )
            }
    missing_values = {}

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        if missing_count > 0:

            missing_percentage = (
                missing_count / len(df) * 100
                if len(df) > 0
                else 0
            )

            missing_values[column] = {
                "count": missing_count,
                "percentage": round(
                    missing_percentage,
                    2
                )
            }

    return {
        "rows": len(df),

        "columns": df.columns.tolist(),

        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "date_columns": date_columns,

        "month_columns": month_columns,

        "date_ranges": date_ranges,

        "missing_values": missing_values
        
    }

def calculate_average(
    df: pd.DataFrame,
    column: str
) -> float:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return float(df[column].mean())


def calculate_sum(
    df: pd.DataFrame,
    column: str
) -> float:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return float(df[column].sum())


def top_n_analysis(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
    n: int = 5,
    ascending: bool = False
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist."
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

    if n <= 0:
        raise ValueError(
            "n must be greater than 0."
        )
    if n > 1000:
        raise ValueError(
            "n cannot be greater than 1000."
        )

    grouped = (
        df.groupby(group_column)[value_column]
        .sum()
        .reset_index()
    )

    result = (
        grouped
        .sort_values(
            value_column,
            ascending=ascending
        )
        .head(n)
    )

    return {
        "analysis_type": "top_n",
        "group_column": group_column,
        "value_column": value_column,
        "n": n,
        "ascending": ascending,
        "selected_values": (
            result[group_column]
            .tolist()
        ),
        "data": result.to_dict(
            orient="records"
        )
    }


def filter_dataframe_by_values(
    df: pd.DataFrame,
    column: str,
    values: list
) -> pd.DataFrame:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    return df[
        df[column].isin(values)
    ].copy()


def group_comparison(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
    aggregation: str = "mean"
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist."
        )

    if aggregation != "count":
        if not pd.api.types.is_numeric_dtype(df[value_column]):
            raise ValueError(
                f"Column '{value_column}' must be numeric."
            )

    if aggregation == "count":

        result = (
        df.groupby(group_column)
        .size()
        .reset_index(name=value_column)
    )


    elif aggregation == "sum":

        grouped = (
            df.groupby(group_column)[value_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        grouped = (
            df.groupby(group_column)[value_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        grouped = (
            df.groupby(group_column)[value_column]
            .count()
            .reset_index()
        )

    else:

        raise ValueError(
            "Aggregation must be sum, mean, or count."
        )

    return {
        "analysis_type": "group_comparison",
        "group_column": group_column,
        "value_column": value_column,
        "aggregation": aggregation,
        "data": grouped.to_dict(
            orient="records"
        )
    }


def percentage_share(
    df: pd.DataFrame,
    group_column: str,
    value_column: str
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist."
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

    grouped = (
        df.groupby(group_column)[value_column]
        .sum()
        .reset_index()
    )

    total = grouped[value_column].sum()

    if total == 0:
        raise ValueError(
            "Cannot calculate percentage share "
            "because the total value is zero."
        )

    grouped["percentage"] = (
        grouped[value_column] / total * 100
    )

    grouped["percentage"] = grouped[
        "percentage"
    ].round(2)

    return {
        "analysis_type": "percentage_share",
        "group_column": group_column,
        "value_column": value_column,
        "total": float(total),
        "data": grouped.to_dict(
            orient="records"
        )
    }

def correlation_analysis(
    df: pd.DataFrame,
    column_x: str,
    column_y: str
) -> dict:

    if column_x not in df.columns:
        raise ValueError(
            f"Column '{column_x}' does not exist."
        )

    if column_y not in df.columns:
        raise ValueError(
            f"Column '{column_y}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column_x]
    ):
        raise ValueError(
            f"Column '{column_x}' must be numeric."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column_y]
    ):
        raise ValueError(
            f"Column '{column_y}' must be numeric."
        )

    data = df[
        [column_x, column_y]
    ].dropna()

    if len(data) < 2:
        raise ValueError(
            "At least two valid observations are "
            "required to calculate correlation."
        )
    if data[column_x].nunique() < 2:
        raise ValueError(
            f"Column '{column_x}' has no variation. "
            "Correlation cannot be calculated."
        )

    if data[column_y].nunique() < 2:
        raise ValueError(
            f"Column '{column_y}' has no variation. "
            "Correlation cannot be calculated."
        )

    correlation = data[
        column_x
    ].corr(
        data[column_y]
    )

    if correlation >= 0.7:
        strength = "strong positive"
    elif correlation >= 0.3:
        strength = "moderate positive"
    elif correlation > -0.3:
        strength = "weak or no linear"
    elif correlation > -0.7:
        strength = "moderate negative"
    else:
        strength = "strong negative"

    return {
        "analysis_type": "correlation",
        "column_x": column_x,
        "column_y": column_y,
        "correlation": round(
            float(correlation),
            4
        ),
        "interpretation": (
            f"The correlation between "
            f"{column_x} and {column_y} is "
            f"{strength}."
        )
    }

def calculate_maximum(
    df: pd.DataFrame,
    column: str
) -> float:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' is not numerical."
        )

    return float(df[column].max())


def calculate_minimum(
    df: pd.DataFrame,
    column: str
) -> float:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' is not numerical."
        )

    return float(df[column].min())


def calculate_count(
    df: pd.DataFrame,
    column: str
) -> int:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    return int(df[column].count())


def filter_data(
    df: pd.DataFrame,
    column: str,
    values: list
) -> dict:

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    filtered_df = df[
        df[column].isin(values)
    ].copy()

    return {
        "analysis_type": "filter",
        "column": column,
        "selected_values": values,
        "rows": len(filtered_df)
    }


def filter_groups_by_metric(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
    aggregation: str,
    operator: str,
    threshold: float
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist."
        )

    if aggregation != "count":
        if not pd.api.types.is_numeric_dtype(
            df[value_column]
        ):
            raise ValueError(
                f"Column '{value_column}' must be numeric."
            )

    if aggregation == "sum":
        grouped = (
            df.groupby(group_column)[value_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":
        grouped = (
            df.groupby(group_column)[value_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "max":
        grouped = (
            df.groupby(group_column)[value_column]
            .max()
            .reset_index()
        )

    elif aggregation == "min":
        grouped = (
            df.groupby(group_column)[value_column]
            .min()
            .reset_index()
        )

    elif aggregation == "count":
        grouped = (
            df.groupby(group_column)
            .size()
            .reset_index(name=value_column)
        )

    else:
        raise ValueError(
            "Aggregation must be sum, mean, max, min, or count."
        )

    if operator == ">":
        filtered = grouped[
            grouped[value_column] > threshold
        ]

    elif operator == ">=":
        filtered = grouped[
            grouped[value_column] >= threshold
        ]

    elif operator == "<":
        filtered = grouped[
            grouped[value_column] < threshold
        ]

    elif operator == "<=":
        filtered = grouped[
            grouped[value_column] <= threshold
        ]

    elif operator == "==":
        filtered = grouped[
            grouped[value_column] == threshold
        ]

    else:
        raise ValueError(
            "Operator must be one of: >, >=, <, <=, =="
        )

    return {
        "analysis_type": "group_filter",
        "group_column": group_column,
        "value_column": value_column,
        "aggregation": aggregation,
        "operator": operator,
        "threshold": threshold,
        "selected_values": (
            filtered[group_column].tolist()
        ),
        "data": filtered.to_dict(
            orient="records"
        )
    }

def group_insight(
    df: pd.DataFrame,
    group_column: str,
    groups: list[str],
    metrics: list[str]
) -> dict:

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist."
        )

    missing_groups = [
        group
        for group in groups
        if group not in df[group_column].astype(str).unique()
    ]

    if missing_groups:
        raise ValueError(
            f"Groups not found in '{group_column}': "
            f"{missing_groups}"
        )

    selected_df = df[
        df[group_column].astype(str).isin(groups)
    ].copy()

    results = []

    for group in groups:

        group_df = selected_df[
            selected_df[group_column].astype(str) == group
        ]

        row = {
            group_column: group,
            "count": int(len(group_df))
        }

        for metric in metrics:

            if metric not in df.columns:
                raise ValueError(
                    f"Column '{metric}' does not exist."
                )

            if not pd.api.types.is_numeric_dtype(
                df[metric]
            ):
                raise ValueError(
                    f"Column '{metric}' must be numeric."
                )

            row[f"{metric}_sum"] = float(
                group_df[metric].sum()
            )

            row[f"{metric}_mean"] = float(
                group_df[metric].mean()
            )

        results.append(row)

    return {
        "analysis_type": "group_insight",
        "group_column": group_column,
        "groups": groups,
        "metrics": metrics,
        "data": results
    }