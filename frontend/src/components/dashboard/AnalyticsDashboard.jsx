import { useEffect, useState } from "react";

import {
  getDashboardSummary,
  getDashboardVisualizations,
} from "../../services/api";

import ChartRenderer from "../ChartRenderer";


function AnalyticsDashboard({ dataset })  {

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [visualizations, setVisualizations] = useState([]);
  const loadDashboard = async () => {
    setLoading(true);
    setError("");

    try {
        const [summary, visualizationData] = await Promise.all([
        getDashboardSummary(),
        getDashboardVisualizations(),
        ]);

        setDashboard(summary);
        setVisualizations(visualizationData.charts || []);
    } catch (error) {
        setError(error.message);
    } finally {
        setLoading(false);
    }
    };


   useEffect(() => {

    if (!dataset) {
        return;
    }

    loadDashboard();

    }, [dataset]);


  if (loading) {
    return (
      <section className="analytics-dashboard">
        <div className="dashboard-loading">
          Loading analytics...
        </div>
      </section>
    );
  }


  if (error) {
    return (
      <section className="analytics-dashboard">
        <div className="dashboard-error">
          {error}
        </div>
      </section>
    );
  }


  if (!dashboard) {
    return null;
  }


  return (
    <section className="analytics-dashboard">

        <nav className="dashboard-nav">

            <button
                onClick={() =>
                document
                    .getElementById("overview")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
            >
            Overview
        </button>

        <button
            onClick={() =>
            document
                .getElementById("data-quality")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            Data Quality
        </button>

        <button
            onClick={() =>
            document
                .getElementById("kpis")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            KPIs
        </button>

        <button
            onClick={() =>
            document
                .getElementById("eda")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            EDA
        </button>

        <button
            onClick={() =>
            document
                .getElementById("visualizations")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            Visualizations
        </button>

        <button
            onClick={() =>
            document
                .getElementById("relationships")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            Relationships
        </button>

        <button
            onClick={() =>
            document
                .getElementById("categories")
                ?.scrollIntoView({ behavior: "smooth" })
            }
        >
            Categories
        </button>

        </nav>
        <div
            id="overview"
            className="dashboard-section-header">
            <div>
                
          <span className="section-eyebrow">
            DATASET OVERVIEW
          </span>

          <h2>Analytics Overview</h2>

          <p>
            Automatic analysis of your uploaded dataset.
          </p>
        </div>
      </div>


      <div className="overview-grid">

        <div className="overview-card">
          <span>Rows</span>
          <strong>{dashboard.rows}</strong>
        </div>

        <div className="overview-card">
          <span>Columns</span>
          <strong>{dashboard.columns}</strong>
        </div>

        <div className="overview-card">
          <span>Numerical</span>
          <strong>
            {dashboard.numerical_columns.length}
          </strong>
        </div>

        <div className="overview-card">
          <span>Categorical</span>
          <strong>
            {dashboard.categorical_columns.length}
          </strong>
        </div>

        <div className="overview-card">
          <span>Missing Cells</span>
          <strong>
            {dashboard.data_quality.missing_cells}
          </strong>
        </div>

      </div>

      <div
        id="data-quality"
        className="dashboard-two-column"
        >

        <div className="dashboard-card">

            <div className="dashboard-card-header">
            <div>
                <span className="section-eyebrow">
                DATA QUALITY
                </span>

                <h3>Dataset Health</h3>
            </div>

            <div className="quality-score">
                {dashboard.data_quality.score}%
            </div>
            </div>

            <div className="quality-stats">

            <div className="quality-stat">
                <span>Missing Cells</span>
                <strong>
                {dashboard.data_quality.missing_cells}
                </strong>
            </div>

            <div className="quality-stat">
                <span>Duplicate Rows</span>
                <strong>
                {dashboard.data_quality.duplicate_rows}
                </strong>
            </div>

            <div className="quality-stat">
                <span>Total Cells</span>
                <strong>
                {dashboard.data_quality.total_cells}
                </strong>
            </div>

            </div>

        </div>
        <div className="dashboard-card">

            <div className="dashboard-card-header">
            <div>
                <span className="section-eyebrow">
                MISSING VALUES
                </span>

                <h3>Data Completeness</h3>
            </div>
            </div>

            <div className="missing-list">

            {Object.entries(
                dashboard.missing_details
            )
                .filter(
                ([, info]) => info.count > 0
                )
                .map(
                ([column, info]) => (

                    <div
                    key={column}
                    className="missing-row"
                    >

                    <span>{column}</span>

                    <strong>
                        {info.count} ({info.percentage}%)
                    </strong>

                    </div>

                )
                )}

            {Object.entries(
                dashboard.missing_details
            ).every(
                ([, info]) => info.count === 0
            ) && (
                <div className="no-missing-data">
                ✓ No missing values detected
                </div>
            )}

            </div>

        </div>

        </div>

        <div
            id="kpis"
            className="dashboard-section"
            >

            <div id="overview" className="dashboard-section-header">
                <div>
                <span className="section-eyebrow">
                    AUTOMATIC KPI DETECTION
                </span>

                <h2>Key Performance Indicators</h2>

                <p>
                    Automatically detected metrics from numerical columns.
                </p>
                </div>
            </div>

            <div className="kpi-grid">

                {Object.entries(dashboard.kpis).map(
                ([column, metrics]) => (

                    <div
                    key={column}
                    className="kpi-card"
                    >

                    <div className="kpi-card-header">
                        <span>
                        {column}
                        </span>

                        <span className="kpi-badge">
                        KPI
                        </span>
                    </div>

                    <div className="kpi-value">
                        {metrics.sum.toLocaleString()}
                    </div>

                    <div className="kpi-secondary">
                        Average:{" "}
                        {metrics.average.toLocaleString()}
                    </div>

                    </div>

                )
                )}

            </div>

            </div>
        <div
            id="eda"
            className="dashboard-section"
            >

            <div id="exploratory-data-analysis" className="dashboard-section-header">
                <div>
                <span className="section-eyebrow">
                    EXPLORATORY DATA ANALYSIS
                </span>

                <h2>Numerical Statistics</h2>

                <p>
                    Statistical summary of numerical columns.
                </p>
                </div>
            </div>

        <div className="dashboard-card eda-card">

                <div className="eda-table-wrapper">

                <table className="eda-table">

                    <thead>
                    <tr>
                        <th>Column</th>
                        <th>Count</th>
                        <th>Mean</th>
                        <th>Median</th>
                        <th>Std Dev</th>
                        <th>Min</th>
                        <th>Max</th>
                    </tr>
                    </thead>

                    <tbody>

                    {Object.entries(
                        dashboard.numerical_statistics
                    ).map(([column, stats]) => (

                        <tr key={column}>

                        <td className="eda-column-name">
                            {column}
                        </td>

                        <td>
                            {stats.count.toLocaleString()}
                        </td>

                        <td>
                            {stats.mean.toLocaleString()}
                        </td>

                        <td>
                            {stats.median.toLocaleString()}
                        </td>

                        <td>
                            {stats.std.toLocaleString()}
                        </td>

                        <td>
                            {stats.min.toLocaleString()}
                        </td>

                        <td>
                            {stats.max.toLocaleString()}
                        </td>

                        </tr>

                    ))}

                    </tbody>

                </table>

                </div>

            </div>

            </div>

        <div
            id="visualizations"
            className="dashboard-section"
            >

    <div id="automatic-visualizations" className="dashboard-section-header">
        <div>
        <span className="section-eyebrow">
            AUTOMATIC VISUALIZATIONS
        </span>

        <h2>Data Visualizations</h2>

        <p>
            Automatically generated charts based on the dataset structure.
        </p>
        </div>
    </div>

    <div className="dashboard-chart-grid">

        {visualizations.map((chart, index) => (
        <div
            key={`${chart.title}-${index}`}
            className="dashboard-chart-item"
        >
            <ChartRenderer chart={chart} />
        </div>
        ))}

    </div>

    </div>

    <div
        id="relationships"
        className="dashboard-section"
        >

    <div id="relationship-analysis" className="dashboard-section-header">
        <div>
        <span className="section-eyebrow">
            RELATIONSHIP ANALYSIS
        </span>

        <h2>Variable Relationships</h2>

        <p>
            Correlation analysis across numerical variables.
        </p>
        </div>
    </div>

    <div
        id="data-quality"
        className="dashboard-two-column"
        >

        <div className="dashboard-card">

        <div className="dashboard-card-header">
            <div>
            <span className="section-eyebrow">
                CORRELATION MATRIX
            </span>

            <h3>Numerical Relationships</h3>
            </div>
        </div>

        <div className="correlation-wrapper">

            <table className="correlation-table">

            <thead>
                <tr>
                <th></th>

                {dashboard.numerical_columns.map(
                    (column) => (
                    <th key={column}>
                        {column}
                    </th>
                    )
                )}
                </tr>
            </thead>

            <tbody>

                {dashboard.numerical_columns.map(
                (row) => (

                    <tr key={row}>

                    <th>{row}</th>

                    {dashboard.numerical_columns.map(
                        (column) => {

                        const value =
                            dashboard
                            .correlation_matrix
                            ?.[
                                row
                            ]?.[
                                column
                            ] ?? 0;

                        return (
                            <td
                            key={column}
                            className={
                                Math.abs(value) >= 0.7
                                ? "correlation-strong"
                                : ""
                            }
                            >
                            {Number(value).toFixed(2)}
                            </td>
                        );
                        }
                    )}

                    </tr>
                )
                )}

            </tbody>

            </table>

        </div>

        </div>


        <div className="dashboard-card">

            <div className="dashboard-card-header">
                <div>
                <span className="section-eyebrow">
                    KEY RELATIONSHIP
                </span>

                <h3>Strongest Correlation</h3>
                </div>
            </div>

            <div className="relationship-highlight">

                {(() => {

                let strongest = null;

                const columns =
                    dashboard.numerical_columns;

                for (let i = 0; i < columns.length; i++) {

                    for (
                    let j = i + 1;
                    j < columns.length;
                    j++
                    ) {

                    const x = columns[i];
                    const y = columns[j];

                    const value =
                        dashboard
                        .correlation_matrix
                        ?.[
                            x
                        ]?.[
                            y
                        ];

                    if (
                        value === undefined ||
                        value === null
                    ) {
                        continue;
                    }

                    if (
                        !strongest ||
                        Math.abs(value) >
                        Math.abs(strongest.value)
                    ) {
                        strongest = {
                        x,
                        y,
                        value
                        };
                    }
                    }

                }

                if (!strongest) {
                    return (
                    <p>
                        Not enough numerical variables
                        for relationship analysis.
                    </p>
                    );
                }

                return (
                    <>
                    <div className="relationship-value">
                        {strongest.value.toFixed(2)}
                    </div>

                    <div className="relationship-label">
                        {strongest.x} ↔ {strongest.y}
                    </div>

                    <p>
                        {Math.abs(strongest.value) >= 0.7
                        ? "Strong linear relationship detected."
                        : "Moderate or weak relationship detected."}
                    </p>
                    </>
                );

                })()}

            </div>

            </div>

        </div>

        </div>

        <div
            id="categories"
            className="dashboard-section"
            >

        <div id="categorical-insights" className="dashboard-section-header">
            <div>
            <span className="section-eyebrow">
                AUTOMATIC CATEGORICAL ANALYSIS
            </span>

            <h2>Categorical Insights</h2>

            <p>
                Automatically detected patterns across categorical variables.
            </p>
            </div>
        </div>

        <div className="categorical-grid">

            {Object.entries(
            dashboard.categorical_analysis
            ).map(([column, analysis]) => (

            <div
                key={column}
                className="dashboard-card categorical-card"
            >

                <div className="dashboard-card-header">

                <div>
                    <span className="section-eyebrow">
                    CATEGORY
                    </span>

                    <h3>{column}</h3>
                </div>

                <span className="unique-badge">
                    {analysis.unique_values} unique
                </span>

                </div>

                <div className="categorical-top">

                <span>Most frequent</span>

                <strong>
                    {analysis.top_value || "None"}
                </strong>

                <small>
                    {analysis.top_count.toLocaleString()} records
                </small>

                </div>

                <div className="categorical-list">

                {analysis.top_values
                    .slice(0, 5)
                    .map((item) => (

                    <div
                        key={item.value}
                        className="categorical-row"
                    >

                        <span>
                        {item.value}
                        </span>

                        <strong>
                        {item.count}
                        </strong>

                    </div>

                    ))}

                </div>

            </div>

            ))}

        </div>

        </div> 
    </section>
  );
}


export default AnalyticsDashboard;

