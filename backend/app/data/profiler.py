import pandas as pd


MONTH_NAMES = {
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
    "dec", "december",
}


def profile_dataset(df: pd.DataFrame) -> dict:

    rows, column_count = df.shape

    numerical_columns = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(
            include=["object", "category", "string"]
        )
        .columns
        .tolist()
    )

    date_columns = []
    month_columns = []

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

            if (
                not values.empty
                and values.isin(MONTH_NAMES).all()
            ):
                month_columns.append(column)
                continue

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            if converted.notna().mean() >= 0.8:
                date_columns.append(column)

    categorical_columns = [
        column
        for column in categorical_columns
        if column not in date_columns
        and column not in month_columns
    ]

    missing_values = {
        column: int(df[column].isna().sum())
        for column in df.columns
    }

    missing_details = {}

    for column in df.columns:

        count = int(df[column].isna().sum())

        percentage = (
            round((count / rows) * 100, 2)
            if rows > 0
            else 0
        )

        missing_details[column] = {
            "count": count,
            "percentage": percentage
        }

    duplicate_rows = int(
        df.duplicated().sum()
    )

    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # Date ranges
    date_ranges = {}

    for column in date_columns:

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_dates = converted.dropna()

        if not valid_dates.empty:
            date_ranges[column] = {
                "min": valid_dates.min().strftime(
                    "%Y-%m-%d"
                ),
                "max": valid_dates.max().strftime(
                    "%Y-%m-%d"
                )
            }

    # Numerical statistics
    numerical_statistics = {}

    if numerical_columns:

        stats = df[
            numerical_columns
        ].describe().T

        for column in numerical_columns:

            numerical_statistics[column] = {
                "count": int(
                    df[column].count()
                ),
                "mean": round(
                    float(stats.loc[column, "mean"]),
                    2
                ),
                "median": round(
                    float(df[column].median()),
                    2
                ),
                "std": round(
                    float(stats.loc[column, "std"]),
                    2
                ) if pd.notna(
                    stats.loc[column, "std"]
                ) else 0,
                "min": float(
                    stats.loc[column, "min"]
                ),
                "max": float(
                    stats.loc[column, "max"]
                )
            }

    # Automatic KPI detection
    kpis = {}

    for column in numerical_columns:

        kpis[column] = {
            "sum": round(
                float(df[column].sum()),
                2
            ),
            "average": round(
                float(df[column].mean()),
                2
            )
        }

    # Correlation matrix
    correlation_matrix = {}

    if len(numerical_columns) >= 2:

        correlation = (
            df[numerical_columns]
            .corr()
            .round(2)
        )

        correlation_matrix = (
            correlation.to_dict()
        )

    # Data quality score
    total_cells = rows * column_count

    missing_cells = sum(
        item["count"]
        for item in missing_details.values()
    )

    missing_ratio = (
        missing_cells / total_cells
        if total_cells > 0
        else 0
    )

    duplicate_ratio = (
        duplicate_rows / rows
        if rows > 0
        else 0
    )

    quality_score = max(
        0,
        round(
            100
            - (missing_ratio * 70)
            - (duplicate_ratio * 30),
            1
        )
    )

    categorical_analysis = {}

    for column in categorical_columns:

        value_counts = (
            df[column]
            .value_counts(dropna=False)
        )

        top_values = []

        for value, count in value_counts.head(10).items():

            display_value = (
                "Missing"
                if pd.isna(value)
                else str(value)
            )

            top_values.append({
                "value": display_value,
                "count": int(count),
                "percentage": round(
                    float(count / len(df) * 100),
                    2
                ) if len(df) > 0 else 0
            })

        categorical_analysis[column] = {
            "unique_values": int(
                df[column].nunique(dropna=True)
            ),
            "top_value": (
                top_values[0]["value"]
                if top_values
                else None
            ),
            "top_count": (
                top_values[0]["count"]
                if top_values
                else 0
            ),
            "top_values": top_values
        }

    return {
        "rows": rows,
        "columns": column_count,
        "column_names": df.columns.tolist(),

        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,

        "date_columns": date_columns,
        "month_columns": month_columns,
        "date_ranges": date_ranges,

        "missing_values": missing_values,
        "missing_details": missing_details,

        "duplicate_rows": duplicate_rows,

        "data_types": data_types,

        "numerical_statistics": numerical_statistics,

        "kpis": kpis,

        "correlation_matrix": correlation_matrix,

        "data_quality": {
            "score": quality_score,
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "duplicate_rows": duplicate_rows
        },
        "categorical_analysis": categorical_analysis
    }