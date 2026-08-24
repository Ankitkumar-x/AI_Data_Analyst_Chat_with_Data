def create_metric_bar_chart(
    df,
    metrics: list,
    title: str
) -> dict:

    data = []

    for metric in metrics:

        data.append(
            {
                "Metric": metric["metric_name"],
                "Value": float(metric["value"])
            }
        )

    return {
        "chart_type": "bar",
        "title": title,
        "x_axis": "Metric",
        "y_axis": "Value",
        "aggregation": "value",
        "data": data
    }