import json

from app.tools.analysis_tools import (
    calculate_average,
    calculate_sum,
    filter_data,
    get_dataset_summary,
    top_n_analysis,
    group_comparison,
    percentage_share,
    correlation_analysis,
    calculate_maximum,
    calculate_minimum,
    calculate_count,
    group_insight,
    filter_groups_by_metric
)

from app.tools.chart_tools import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot
)

from app.tools.metric_chart_tools import (
    create_metric_bar_chart
)

AVAILABLE_FUNCTIONS = {
    "calculate_average": calculate_average,
    "calculate_sum": calculate_sum,
    "get_dataset_summary": get_dataset_summary,
    "create_bar_chart": create_bar_chart,
    "create_line_chart": create_line_chart,
    "create_pie_chart": create_pie_chart,
    "create_scatter_plot": create_scatter_plot,
    "top_n_analysis": top_n_analysis,
    "group_comparison": group_comparison,
    "percentage_share": percentage_share,
    "correlation_analysis": correlation_analysis,
    "create_metric_bar_chart": create_metric_bar_chart,
    "calculate_maximum": calculate_maximum,
    "calculate_minimum": calculate_minimum,
    "calculate_count": calculate_count,
    "group_insight": group_insight,
    "filter_data": filter_data,
    "filter_groups_by_metric": filter_groups_by_metric,
}

import json


def execute_tool_call(
    tool_call,
    df
):

    function_name = tool_call.function.name

    function_args = json.loads(
        tool_call.function.arguments
    )

    if df.empty:
        return {
            "error": (
                "The dataset is empty. "
                "Please upload a dataset containing "
                "at least one row."
            )
        }

    if function_name not in AVAILABLE_FUNCTIONS:
        return {
            "error": (
                f"Unknown tool: {function_name}"
            )
        }

    function_to_call = (
        AVAILABLE_FUNCTIONS[function_name]
    )

    try:
        missing_columns = {}

        for column in df.columns:
            missing_count = int(
                df[column].isna().sum()
            )

            if missing_count > 0:
                missing_columns[column] = missing_count

        result = function_to_call(
            df,
            **function_args
        )

        if isinstance(result, dict) and missing_columns:
            result["missing_values"] = missing_columns

        return result

    except ValueError as error:

        numeric_columns = (
            df.select_dtypes(
                include="number"
            )
            .columns
            .tolist()
        )

        return {
            "error": str(error),
            "available_columns": df.columns.tolist(),
            "numeric_columns": numeric_columns
        }

    except Exception as error:

        return {
            "error": (
                "An unexpected error occurred "
                "while analyzing the dataset."
            )
        }