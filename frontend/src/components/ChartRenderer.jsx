import Plot from "react-plotly.js";


function ChartRenderer({ chart }) {

  if (!chart) {
    return null;
  }


  const xValues = chart.data.map(
    (item) => item[chart.x_axis]
  );

  const yValues = chart.data.map(
    (item) => item[chart.y_axis]
  );


  // METRIC BAR CHART
if (
  chart.chart_type === "bar" &&
  chart.aggregation === "value"
) {
  const labels = chart.data.map(
    (item) => item.Metric
  );

  const values = chart.data.map(
    (item) => item.Value
  );

  return (
    <div className="chart-card">

      <div className="chart-card-header">
        <div className="chart-card-title">
          {chart.title}
        </div>

        <div className="chart-card-subtitle">
          Calculated metrics
        </div>
      </div>

      <div className="chart-card-body">

        <Plot
          data={[
            {
              x: labels,
              y: values,
              type: "bar",

              hovertemplate:
                "%{x}: %{y}<extra></extra>",
            },
          ]}

          layout={{
            title: {
              text: chart.title,
            },

            xaxis: {
              title: "Metric",
            },

            yaxis: {
              title: "Value",
            },

            autosize: true,

            margin: {
              l: 70,
              r: 30,
              t: 70,
              b: 70,
            },

            paper_bgcolor: "white",
            plot_bgcolor: "white",
          }}

          config={{
            responsive: true,
            displayModeBar: true,
          }}

          style={{
            width: "100%",
            height: "420px",
          }}
        />

      </div>

    </div>
  );
}


  // BAR CHART
if (chart.chart_type === "bar") {
  const xValues = chart.data.map(
    (item) => item[chart.x_axis]
  );

  const yValues = chart.data.map(
    (item) => item[chart.y_axis]
  );

  return (
    <div className="chart-card">

      <div className="chart-card-header">
        <div className="chart-card-title">
          {chart.title}
        </div>

        <div className="chart-card-subtitle">
          {chart.aggregation
            ? `${chart.aggregation} analysis`
            : "Data visualization"}
        </div>
      </div>

      <div className="chart-card-body">

        <Plot
          data={[
            {
              x: xValues,
              y: yValues,
              type: "bar",

              hovertemplate:
                `${chart.x_axis}: %{x}<br>` +
                `${chart.y_axis}: %{y}<extra></extra>`,
            },
          ]}

          layout={{
            title: {
              text: chart.title,
            },

            xaxis: {
              title: chart.x_axis,
            },

            yaxis: {
              title: chart.y_axis,
            },

            autosize: true,

            margin: {
              l: 70,
              r: 30,
              t: 70,
              b: 70,
            },

            paper_bgcolor: "white",
            plot_bgcolor: "white",
          }}

          config={{
            responsive: true,
            displayModeBar: true,
          }}

          style={{
            width: "100%",
            height: "420px",
          }}
        />

      </div>

    </div>
  );
}


// LINE CHART
if (chart.chart_type === "line") {

  const xValues = chart.data.map(
    (item) => item[chart.x_axis]
  );

  const yValues = chart.data.map(
    (item) => item[chart.y_axis]
  );

  return (
    <div className="chart-card">

      <div className="chart-card-header">
        <div className="chart-card-title">
          {chart.title}
        </div>

        <div className="chart-card-subtitle">
          {chart.aggregation
            ? `${chart.aggregation} analysis`
            : "Data visualization"}
        </div>
      </div>

      <div className="chart-card-body">

        <Plot
          data={[
            {
              x: xValues,
              y: yValues,
              type: "scatter",
              mode: "lines+markers",

              hovertemplate:
                `${chart.x_axis}: %{x}<br>` +
                `${chart.y_axis}: %{y}<extra></extra>`,
            },
          ]}

          layout={{
            title: {
              text: chart.title,
            },

            xaxis: {
              title: chart.x_axis,
            },

            yaxis: {
              title: chart.y_axis,
            },

            autosize: true,

            margin: {
              l: 70,
              r: 30,
              t: 70,
              b: 70,
            },

            paper_bgcolor: "white",
            plot_bgcolor: "white",
          }}

          config={{
            responsive: true,
            displayModeBar: true,
          }}

          style={{
            width: "100%",
            height: "420px",
          }}
        />

      </div>

    </div>
  );
}


  // PIE CHART
if (chart.chart_type === "pie") {

  const labels = chart.data.map(
    (item) => item[chart.category_column]
  );

  const values = chart.data.map(
    (item) => item[chart.value_column]
  );

  return (
      <div className="chart-card">

        <div className="chart-card-header">
          <div className="chart-card-title">
            {chart.title}
          </div>

          <div className="chart-card-subtitle">
            {chart.aggregation
              ? `${chart.aggregation} analysis`
              : "Data visualization"}
          </div>
        </div>

        <div className="chart-card-body">

          <Plot
            data={[
              {
                labels: labels,
                values: values,
                type: "pie",

                textinfo: "label+percent",

                hovertemplate:
                  "%{label}<br>" +
                  `${chart.value_column}: %{value}` +
                  "<br>Percentage: %{percent}" +
                  "<extra></extra>",
              },
            ]}

            layout={{
              title: {
                text: chart.title,
              },

              autosize: true,

              margin: {
                l: 30,
                r: 30,
                t: 70,
                b: 30,
              },

              paper_bgcolor: "white",
            }}

            config={{
              responsive: true,
              displayModeBar: true,
            }}

            style={{
              width: "100%",
              height: "420px",
            }}
          />

        </div>

      </div>
    );
  }


// SCATTER PLOT
if (chart.chart_type === "scatter") {

  const xValues = chart.data.map(
    (item) => item[chart.x_axis]
  );

  const yValues = chart.data.map(
    (item) => item[chart.y_axis]
  );

  return (
    <div className="chart-card">

      <div className="chart-card-header">
        <div className="chart-card-title">
          {chart.title}
        </div>

        <div className="chart-card-subtitle">
          Relationship between {chart.x_axis} and {chart.y_axis}
        </div>
      </div>

      <div className="chart-card-body">

        <Plot
          data={[
            {
              x: xValues,
              y: yValues,
              type: "scatter",
              mode: "markers",

              hovertemplate:
                `${chart.x_axis}: %{x}<br>` +
                `${chart.y_axis}: %{y}` +
                "<extra></extra>",
            },
          ]}

          layout={{
            title: {
              text: chart.title,
            },

            xaxis: {
              title: chart.x_axis,
            },

            yaxis: {
              title: chart.y_axis,
            },

            autosize: true,

            margin: {
              l: 70,
              r: 30,
              t: 70,
              b: 70,
            },

            paper_bgcolor: "white",
            plot_bgcolor: "white",
          }}

          config={{
            responsive: true,
            displayModeBar: true,
          }}

          style={{
            width: "100%",
            height: "420px",
          }}
        />

      </div>

    </div>
  );
}


  // Unsupported chart
  return (
    <div className="unsupported-chart">

      Unsupported chart type:
      {" "}
      {chart.chart_type}

    </div>
  );
}


export default ChartRenderer;