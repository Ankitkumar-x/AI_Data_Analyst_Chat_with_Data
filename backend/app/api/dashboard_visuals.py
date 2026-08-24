from fastapi import APIRouter, HTTPException
import pandas as pd
from app.data.dataset_manager import get_active_dataset


router = APIRouter()


@router.get("/dashboard/visualizations")
async def dashboard_visualizations():

    try:
        df = get_active_dataset()

        charts = []

        # Sales by Category
        if "Category" in df.columns and "Sales" in df.columns:
            grouped = (
                df.groupby("Category")["Sales"]
                .sum()
                .reset_index()
            )

            charts.append({
                "chart_type": "bar",
                "title": "Sales by Category",
                "x_axis": "Category",
                "y_axis": "Sales",
                "aggregation": "sum",
                "data": grouped.to_dict(
                    orient="records"
                )
            })

        # Sales by Month
        if "Month" in df.columns and "Sales" in df.columns:

            month_order = [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec"
            ]

            grouped = (
                df.groupby("Month")["Sales"]
                .sum()
                .reset_index()
            )

            grouped["Month"] = pd.Categorical(
                grouped["Month"],
                categories=month_order,
                ordered=True
            )

            grouped = grouped.sort_values("Month")

            grouped["Month"] = grouped["Month"].astype(str)

            charts.append({
                "chart_type": "line",
                "title": "Sales Trend by Month",
                "x_axis": "Month",
                "y_axis": "Sales",
                "aggregation": "sum",
                "data": grouped.to_dict(
                    orient="records"
                )
            })

        # Profit by Category
        if "Category" in df.columns and "Profit" in df.columns:

            grouped = (
                df.groupby("Category")["Profit"]
                .sum()
                .reset_index()
            )

            charts.append({
                "chart_type": "bar",
                "title": "Profit by Category",
                "x_axis": "Category",
                "y_axis": "Profit",
                "aggregation": "sum",
                "data": grouped.to_dict(
                    orient="records"
                )
            })

        # Sales vs Profit
        if "Sales" in df.columns and "Profit" in df.columns:

            charts.append({
                "chart_type": "scatter",
                "title": "Sales vs Profit",
                "x_axis": "Sales",
                "y_axis": "Profit",
                "data": df[
                    ["Sales", "Profit"]
                ].to_dict(
                    orient="records"
                )
            })

        return {
            "charts": charts
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )