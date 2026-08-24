calculate_average_tool = {
    "type": "function",
    "function": {
        "name": "calculate_average",
        "description": (
            "Calculate the average value of a numerical "
            "column in the user's dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The name of the numerical column "
                        "to calculate the average for."
                    )
                }
            },
            "required": ["column"]
        }
    }
}


calculate_sum_tool = {
    "type": "function",
    "function": {
        "name": "calculate_sum",
        "description": (
            "Calculate the total sum of a numerical "
            "column in the user's dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The name of the numerical column "
                        "to calculate the sum for."
                    )
                }
            },
            "required": ["column"]
        }
    }
}


get_dataset_summary_tool = {
    "type": "function",
    "function": {
        "name": "get_dataset_summary",
        "description": (
            "Get the number of rows, column names, "
            "and data types of the user's dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}



create_bar_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_bar_chart",
        "description": (
            "Create a bar chart by grouping a categorical "
            "column and aggregating a numerical column."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category_column": {
                    "type": "string",
                    "description": (
                        "The categorical column used "
                        "for the x-axis."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column used "
                        "for the y-axis."
                    )
                },
                "aggregation": {
                    "type": "string",
                    "enum": [
                        "sum",
                        "mean",
                        "count"
                    ],
                    "description": (
                        "Aggregation method to use."
                    )
                }
            },
            "required": [
                "category_column",
                "value_column"
            ]
        }
    }
}


create_line_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_line_chart",
        "description": (
            "Create a line chart showing how a numerical "
            "value changes across an ordered or time-based "
            "column."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "x_column": {
                    "type": "string",
                    "description": (
                        "The ordered or time-based column "
                        "used for the x-axis."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column used "
                        "for the y-axis."
                    )
                },
                "aggregation": {
                    "type": "string",
                    "enum": [
                        "sum",
                        "mean",
                        "count"
                    ],
                    "description": (
                        "Aggregation method to use."
                    )
                }
            },
            "required": [
                "x_column",
                "value_column"
            ]
        }
    }
}

create_pie_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_pie_chart",
        "description": (
            "Create a pie chart showing the distribution "
            "of a numerical value across categories."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category_column": {
                    "type": "string",
                    "description": (
                        "The categorical column used "
                        "for the pie chart slices."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column whose "
                        "values determine slice sizes."
                    )
                },
                "aggregation": {
                    "type": "string",
                    "enum": [
                        "sum",
                        "mean",
                        "count"
                    ],
                    "description": (
                        "Aggregation method to use."
                    )
                }
            },
            "required": [
                "category_column",
                "value_column"
            ]
        }
    }
}

create_scatter_plot_tool = {
    "type": "function",
    "function": {
        "name": "create_scatter_plot",
        "description": (
            "Create a scatter plot showing the relationship "
            "between two numerical columns."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "x_column": {
                    "type": "string",
                    "description": (
                        "The numerical column used "
                        "for the x-axis."
                    )
                },
                "y_column": {
                    "type": "string",
                    "description": (
                        "The numerical column used "
                        "for the y-axis."
                    )
                }
            },
            "required": [
                "x_column",
                "y_column"
            ]
        }
    }
}

top_n_analysis_tool = {
    "type": "function",
    "function": {
        "name": "top_n_analysis",
        "description": (
            "Find the top or bottom N groups based on "
            "the total value of a numerical column. "
            "Use this for questions such as top products "
            "by sales or lowest regions by profit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "group_column": {
                    "type": "string",
                    "description": (
                        "The categorical column used "
                        "to group the data."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column used "
                        "for ranking."
                    )
                },
                "n": {
                    "type": "integer",
                    "description": (
                        "Number of groups to return."
                    )
                },
                "ascending": {
                    "type": "boolean",
                    "description": (
                        "False for highest values first "
                        "and True for lowest values first."
                    )
                }
            },
            "required": [
                "group_column",
                "value_column"
            ]
        }
    }
}


group_comparison_tool = {
    "type": "function",
    "function": {
        "name": "group_comparison",
        "description": (
            "Compare a numerical value across groups using "
            "mean, sum, max, min, or count. For count, the "
            "value column does not need to be numerical; count "
            "the number of rows in each group."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "group_column": {
                    "type": "string",
                    "description": (
                        "The categorical column used "
                        "to create groups."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column to compare."
                    )
                },
                "aggregation": {
                    "type": "string",
                    "enum": [
                        "sum",
                        "mean",
                        "count"
                    ],
                    "description": (
                        "Aggregation method. Use mean for "
                        "average, sum for total, and count "
                        "for number of records."
                    )
                }
            },
            "required": [
                "group_column",
                "value_column",
                "aggregation"
            ]
        }
    }
}


percentage_share_tool = {
    "type": "function",
    "function": {
        "name": "percentage_share",
        "description": (
            "Calculate each group's percentage contribution "
            "to the total of a numerical column. Use this "
            "for questions about percentage, share, "
            "contribution, or proportion."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "group_column": {
                    "type": "string",
                    "description": (
                        "The categorical column used "
                        "to create groups."
                    )
                },
                "value_column": {
                    "type": "string",
                    "description": (
                        "The numerical column whose "
                        "percentage contribution is calculated."
                    )
                }
            },
            "required": [
                "group_column",
                "value_column"
            ]
        }
    }
}


correlation_analysis_tool = {
    "type": "function",
    "function": {
        "name": "correlation_analysis",
        "description": (
            "Calculate the Pearson correlation between "
            "two numerical columns and interpret the "
            "strength and direction of their linear relationship."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column_x": {
                    "type": "string",
                    "description": (
                        "The first numerical column."
                    )
                },
                "column_y": {
                    "type": "string",
                    "description": (
                        "The second numerical column."
                    )
                }
            },
            "required": [
                "column_x",
                "column_y"
            ]
        }
    }
}

create_metric_bar_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_metric_bar_chart",
        "description": (
            "Create a bar chart comparing one or more "
            "calculated metric values, such as average "
            "Sales and average Profit. Use this tool when "
            "the user asks to visualize calculated scalar "
            "metrics rather than values grouped by a dataset column."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "metrics": {
                    "type": "array",
                    "description": (
                        "Calculated metrics to display in the chart."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "metric_name": {
                                "type": "string",
                                "description": (
                                    "Name of the calculated metric."
                                )
                            },
                            "value": {
                                "type": "number",
                                "description": (
                                    "Calculated numeric value."
                                )
                            }
                        },
                        "required": [
                            "metric_name",
                            "value"
                        ]
                    }
                },
                "title": {
                    "type": "string",
                    "description": "Chart title."
                }
            },
            "required": [
                "metrics",
                "title"
            ]
        }
    }
}


calculate_maximum_tool = {
    "type": "function",
    "function": {
        "name": "calculate_maximum",
        "description": (
            "Return the maximum value of a numerical "
            "column in the dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The numerical column to analyze."
                    )
                }
            },
            "required": [
                "column"
            ]
        }
    }
}

calculate_minimum_tool = {
    "type": "function",
    "function": {
        "name": "calculate_minimum",
        "description": (
            "Return the minimum value of a numerical "
            "column in the dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The numerical column to analyze."
                    )
                }
            },
            "required": [
                "column"
            ]
        }
    }
}

calculate_count_tool = {
    "type": "function",
    "function": {
        "name": "calculate_count",
        "description": (
            "Return the number of non-missing values "
            "in a dataset column."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The column to count."
                    )
                }
            },
            "required": [
                "column"
            ]
        }
    }
}


filter_data_tool = {
    "type": "function",
    "function": {
        "name": "filter_data",
        "description": (
            "Filter the dataset to rows where a categorical "
            "column matches one or more specified values. "
            "Use this before another analysis when the user "
            "specifies a condition such as Category = Technology "
            "or Region = West."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": (
                        "The column to filter."
                    )
                },
                "values": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "The values that should be retained."
                    )
                }
            },
            "required": [
                "column",
                "values"
            ]
        }
    }
}

filter_groups_by_metric_tool = {
    "type": "function",
    "function": {
        "name": "filter_groups_by_metric",
        "description": (
            "Filter groups based on an aggregated metric. "
            "Use this tool repeatedly when a question contains "
            "multiple conditions. Each call can apply one condition "
            "to the current working dataset, and subsequent calls "
            "must operate on the filtered result."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "group_column": {
                    "type": "string"
                },
                "value_column": {
                    "type": "string"
                },
                "aggregation": {
                    "type": "string",
                    "enum": [
                        "sum",
                        "mean",
                        "max",
                        "min",
                        "count"
                    ]
                },
                "operator": {
                    "type": "string",
                    "enum": [
                        ">",
                        ">=",
                        "<",
                        "<=",
                        "=="
                    ]
                },
                "threshold": {
                    "type": "number"
                }
            },
            "required": [
                "group_column",
                "value_column",
                "aggregation",
                "operator",
                "threshold"
            ]
        }
    }
}

group_insight_tool = {
    "type": "function",
    "function": {
        "name": "group_insight",
        "description": (
            "Compare specific groups using multiple numerical "
            "metrics. Use this for questions asking why one "
            "category, region, or group performs differently "
            "from another group."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "group_column": {
                    "type": "string",
                    "description": (
                        "The categorical column containing "
                        "the groups to compare."
                    )
                },
                "groups": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "The groups to compare."
                    )
                },
                "metrics": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Numerical columns to compare."
                    )
                }
            },
            "required": [
                "group_column",
                "groups",
                "metrics"
            ]
        }
    }
}

AVAILABLE_TOOLS = [
    calculate_average_tool,
    calculate_sum_tool,
    calculate_maximum_tool,
    calculate_minimum_tool,
    calculate_count_tool,
    filter_data_tool,
    filter_groups_by_metric_tool,

    calculate_count_tool,

    get_dataset_summary_tool,
    group_insight_tool,
    create_bar_chart_tool,
    create_line_chart_tool,
    create_pie_chart_tool,
    create_scatter_plot_tool,
    create_metric_bar_chart_tool,

    top_n_analysis_tool,
    group_comparison_tool,
    percentage_share_tool,
    correlation_analysis_tool
]