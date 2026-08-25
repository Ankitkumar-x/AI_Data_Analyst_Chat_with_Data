import json
import pandas as pd

from app.ai.groq_client import client
from app.ai.tool_schemas import AVAILABLE_TOOLS
from app.ai.tool_executor import execute_tool_call

from app.tools.analysis_tools import (
    filter_dataframe_by_values
)

MODEL_NAME = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are an AI Data Analyst.

Your job is to answer questions about the user's dataset.

Important rules:

1. Use the available tools whenever the question requires
   calculations or information from the dataset.

2. Never invent numerical results.

3. If a requested column does not exist, explain that clearly.

4. Use the dataset tools to obtain accurate results.

5. After receiving a tool result, explain the result clearly
   and concisely to the user.

6. Do not expose internal tool-calling details to the user.

7. When the user asks for a dataset summary, dataset profile,
   or complete profile of the dataset, use get_dataset_summary.

8. get_dataset_summary already provides the dataset profile,
   including rows, columns, data types, numerical columns,
   categorical columns, date columns, date ranges, and
   missing values.

9. When answering a dataset profile request, do not call
   calculation tools such as calculate_sum or calculate_average
   unless the user explicitly asks for those calculations.

10. After receiving a complete dataset summary from
    get_dataset_summary, provide the answer directly.

11. For follow-up questions, use the most recent relevant
    user request and assistant result as the primary context.

12. When the user uses singular references such as "it",
    "that", "this", or "show it", interpret the reference
    as the most recent analysis result unless the user
    explicitly refers to multiple metrics or groups.

13. Do not combine multiple metrics merely because they
    appeared earlier in the conversation.

14. For example, if the conversation is:

    User: What is the average Sales?
    Assistant: Average Sales is 26,250.
    User: What about Profit?
    Assistant: Average Profit is 4,500.
    User: Show it as a bar chart.

    Interpret "it" as Profit, because Profit is the most
    recent analysis result.

15. Only compare Sales and Profit together when the user
    explicitly asks for a comparison, such as:
    "Compare Sales and Profit."

16. When the user asks to visualize a previous result,
    use the most recent relevant metric and analysis context
    to select the appropriate chart tool.       

17. When the user asks to visualize one or more previously
    calculated scalar metrics, use create_metric_bar_chart.

18. A scalar metric is a single calculated value such as
    average Sales, average Profit, total Sales, or total Profit.

19. If the conversation contains multiple recent calculated
    metrics and the user says "show it", "chart it", or
    "visualize it", preserve the most recent relevant metrics
    rather than inventing a dataset grouping column.

20. Use create_bar_chart when the user wants values grouped
    by a dataset column such as Product, Category, or Region.

21. Use create_metric_bar_chart when there is no grouping
    column and the user wants to visualize calculated metrics.

22. Do not ask the user to choose a categorical column merely
    to visualize already calculated scalar metrics.      

23. Determine the user's analytical intent before selecting tools.

24. Common analytical intents include:
    - summary
    - aggregation
    - comparison
    - ranking
    - percentage/share
    - correlation
    - trend
    - distribution
    - filtering
    - visualization
    - multi-step analysis

25. Match the user's wording to the appropriate analytical intent.
    Examples:
    - "total", "sum" → sum/aggregation
    - "average", "mean" → average/aggregation
    - "highest", "top", "best" → ranking
    - "lowest", "bottom", "worst" → ranking
    - "percentage", "share", "contribution" → percentage/share
    - "relationship", "correlation" → correlation
    - "trend over time", "monthly trend" → time/trend analysis
    - "distribution" → distribution analysis
    - "compare" → comparison
    - "show as a chart", "visualize" → visualization

26. Do not choose a tool only because a keyword appears in the
    question. Consider the complete meaning of the question.

27. If a question requires multiple analytical operations,
    perform them in a logical order and use the result of one
    operation when selecting the next tool.

28. If the user asks for both analysis and visualization,
    complete the analysis first and then create the appropriate
    visualization from the result.

29. Never replace a requested calculation with a visualization.
    The numerical analysis must be performed first when the
    question asks for a numerical result.

30. Never invent an aggregation method. Use the method implied
    by the user's wording or the most appropriate analytical
    interpretation.    

31. Use calculate_maximum when the user asks for:
    maximum, highest value, largest value, greatest value,
    peak value, or max.

32. Use calculate_minimum when the user asks for:
    minimum, lowest value, smallest value, least value,
    lowest value, or min.

33. Use calculate_count when the user asks:
    how many records, number of records, count, how many
    values, or number of entries.

34. Do not use calculate_sum or calculate_average as a
    substitute for maximum, minimum, or count.

35. When a numerical column is requested, verify that the
    requested column exists and is numerical before performing
    numerical calculations. 

36. Use filter_data whenever the user specifies a condition
    that restricts which rows should be analyzed.

37. Filtering must happen before aggregation, ranking,
    comparison, percentage calculation, or visualization
    when the user's question contains a data condition.

38. Examples:
    - "Sales in the Technology category"
    - "Products in the West region"
    - "Customers from India"
    - "Transactions where Category is Furniture"

39. For questions involving multiple operations, preserve
    the filtered dataset for subsequent tool calls.

40. Do not answer a filtered analytical question using the
    unfiltered dataset.

41. For a question such as:
    "Show me the top 3 products by Sales in the Technology
    category."

    first filter Category = Technology, then perform the
    top-N analysis on Product using Sales.       

42. When the user specifies a condition on an aggregated
    group metric, use filter_groups_by_metric.

43. Examples:
    - "regions with Sales above 10000"
    - "categories with average Profit below 5000"
    - "products with more than 5 transactions"

44. Apply group filtering before performing the next
    requested aggregation or ranking.

45. Do not apply the condition mentally or through
    explanation alone. The condition must be enforced
    through the tool result and filtered working dataset.

46. For example:
    "Which region had Sales above 10000 and the highest
    average Profit?"

    First filter regions using:
    group_column = Region
    value_column = Sales
    aggregation = sum
    operator = >
    threshold = 10000

    Then calculate average Profit on the remaining regions.    

47. When a user asks for multiple conditions connected by
    "and", every condition must be evaluated.

48. Conditions must be applied sequentially to the working
    dataset when they refer to the same groups.

49. Example:
    "Which regions have total Sales above 100000 and
    average Profit below 3000?"

    First use filter_groups_by_metric for:
    Region
    Sales
    sum
    >
    100000

    Then apply the second condition to the resulting
    working dataset:

    Region
    Profit
    mean
    <
    3000

50. Never stop after satisfying only the first condition.

51. The final answer must contain only groups that satisfy
    ALL requested conditions.

52. When multiple conditions are present, preserve the
    filtered working dataset after each condition before
    applying the next condition.    

53. Use group_insight for "why", "explain", or performance
    comparison questions involving specific groups.

54. For questions such as:
    "Why does Technology have higher Sales than Furniture?"

    compare the requested groups directly using group_insight.

55. group_insight must analyze the requested groups from the
    original dataset, not from a previously filtered working dataset.

56. Do not sequentially filter one comparison group and then
    attempt to filter another comparison group from that already
    filtered dataset.

57. When explaining why one group differs from another, compare
    measurable metrics such as total, average, and record count.
    Do not claim causation unless the data directly supports it.

58. Distinguish correlation or measurable differences from causal
    explanations. Use phrases such as "is associated with" or
    "has a higher average" when causation cannot be established. 

59. When the user explicitly asks for a percentage, share,
    contribution, or proportion, percentage_share MUST be used.

60. In a multi-step question, every explicitly requested
    analytical operation must be completed before producing
    the final answer.

61. For example, if the user asks:
    "Which category has the highest total Sales, what
    percentage of total Sales does it contribute, why is it
    higher than the second-highest category, and show me a
    bar chart?"

    The required operations are:

    1. Determine category total Sales.
    2. Identify the highest category.
    3. Calculate its percentage of total Sales using
       percentage_share.
    4. Compare the highest category with the second-highest
       category using group_insight.
    5. Create the requested bar chart.

62. Do not skip an explicitly requested operation just because
    another tool already provides a related result.

63. Do not calculate a requested percentage mentally when the
    percentage_share tool is available.       
"""

def build_dataset_context(df: pd.DataFrame) -> str:

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

    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            date_columns.append(column)

        elif pd.api.types.is_string_dtype(
            df[column]
        ):
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
    ]

    missing_values = {
        column: int(df[column].isna().sum())
        for column in df.columns
        if df[column].isna().sum() > 0
    }

    return f"""

DATASET CONTEXT:

Rows: {len(df)}

Columns:
{df.columns.tolist()}

Numerical columns:
{numerical_columns}

Categorical columns:
{categorical_columns}

Date columns:
{date_columns}

Missing values:
{missing_values if missing_values else "None"}
"""

def analyze_question(
        df,
        user_question: str,
        conversation_history=None
) -> dict:

    working_df = df.copy()

    if conversation_history is None:
        conversation_history = []

    dataset_context = build_dataset_context(df)

    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\n"
                + dataset_context
            )
        }
    ]

    MAX_HISTORY_MESSAGES = 16

    recent_history = conversation_history[
        -MAX_HISTORY_MESSAGES:
    ]

    messages.extend(
        recent_history
    )

    messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    chart_data = None

    # Allow the agent to perform multiple tool-calling rounds.
    for _ in range(10):

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=AVAILABLE_TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # The model has finished using tools.
        if not assistant_message.tool_calls:

            return {
                "answer": assistant_message.content,
                "chart": chart_data
            }

        # Add the assistant's tool-call message.
        messages.append(assistant_message)

        # Execute every tool requested by the model.
        for tool_call_index, tool_call in enumerate(
        assistant_message.tool_calls):

            tool_name = tool_call.function.name

            tool_df = working_df

            if tool_call.function.name in [
                "group_insight",
                "percentage_share"
            ]:
                tool_df = df

            tool_result = execute_tool_call(
                tool_call,
                tool_df
            )

            if (
                tool_call.function.name
                == "filter_groups_by_metric"
                and isinstance(tool_result, dict)
                and "group_column" in tool_result
                and "selected_values" in tool_result
            ):

                working_df = filter_dataframe_by_values(
                    working_df,
                    tool_result["group_column"],
                    tool_result["selected_values"]
                )

                print("\nGROUP-FILTERED DATASET:")
                print(
                    "Column:",
                    tool_result["group_column"]
                )
                print(
                    "Values:",
                    tool_result["selected_values"]
                )
                print(
                    "Rows:",
                    len(working_df)
                )

            if (
                tool_call.function.name == "filter_data"
                and isinstance(tool_result, dict)
                and "column" in tool_result
                and "selected_values" in tool_result
            ):

                working_df = filter_dataframe_by_values(
                    working_df,
                    tool_result["column"],
                    tool_result["selected_values"]
                )

                print("\nFILTERED DATASET:")
                print("Column:", tool_result["column"])
                print("Values:", tool_result["selected_values"])
                print("Rows:", len(working_df))

            next_tool_name = None

            if tool_call_index + 1 < len(
                assistant_message.tool_calls
            ):
                next_tool_name = (
                    assistant_message
                    .tool_calls[tool_call_index + 1]
                    .function
                    .name
                )


            if (
                tool_call.function.name == "top_n_analysis"
                and next_tool_name
                in [
                    "create_bar_chart",
                    "create_line_chart",
                    "create_pie_chart",
                    "create_scatter_plot"
                ]
                and isinstance(tool_result, dict)
                and "selected_values" in tool_result
            ):

                working_df = filter_dataframe_by_values(
                    working_df,
                    tool_result["group_column"],
                    tool_result["selected_values"]
                )

            print("\nTOOL USED:")
            print(tool_name)

            print("\nTOOL RESULT:")
            print(tool_result)

            # Save chart data separately.
            if tool_name in [
                "create_bar_chart",
                "create_line_chart",
                "create_pie_chart",
                "create_scatter_plot",
                "create_metric_bar_chart"
            ]:
                chart_data = tool_result

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                }
            )

    # Safety fallback if the model keeps calling tools.
    return {
        "answer": (
            "I was unable to complete the analysis "
            "within the allowed tool steps."
        ),
        "chart": chart_data
    }