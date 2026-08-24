import { useRef, useState } from "react";

import { uploadDataset } from "../services/api";


function DatasetPanel({
  onDatasetLoaded
})  {

  const fileInputRef = useRef(null);

  const [uploading, setUploading] = useState(false);

  const [error, setError] = useState("");

  const [dataset, setDataset] = useState(null);


  const handleChooseFile = () => {

    fileInputRef.current.click();

  };


  const handleFileChange = async (event) => {

    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setError("");

    setUploading(true);

    try {

      const result = await uploadDataset(file);

      setDataset(result);

      if (onDatasetLoaded) {
        onDatasetLoaded(result);
      }

    } catch (error) {

      setError(error.message);

    } finally {

      setUploading(false);

    }
  };


  const getColumnType = (column) => {

    const dataType =
      dataset?.profile?.data_types?.[column];

    if (!dataType) {
      return "Unknown";
    }

    if (
      dataset.profile.numerical_columns.includes(
        column
      )
    ) {
      return "Number";
    }

    if (
      dataset.profile.categorical_columns.includes(
        column
      )
    ) {
      return "Text";
    }

    return dataType;
  };


  return (
    <aside className="dataset-panel">

      <div className="panel-title">

        <h2>Dataset</h2>

        <p>
          Upload your CSV or Excel file
        </p>

      </div>


      <div className="upload-box">

        <div className="upload-icon">
          📊
        </div>

        <h3>Upload Dataset</h3>

        <p>
          Upload a CSV or Excel file to start analyzing
          your data.
        </p>

        <span className="upload-formats">
          CSV · XLSX · XLS
        </span>

        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />

        <button
          className="upload-button"
          onClick={handleChooseFile}
          disabled={uploading}
        >
          {uploading
            ? "Analyzing dataset..."
            : dataset
              ? "Replace Dataset"
              : "Choose File"}
        </button>

      </div>


      {error && (

        <div className="error-message">
          {error}
        </div>

      )}


      {dataset && (

        <div className="dataset-info">

          <div className="dataset-header">
            <div>
              <span className="dataset-status">
                ACTIVE DATASET
              </span>

              <h3>
                {dataset.filename}
              </h3>
            </div>

            <span className="dataset-status-dot">
              ●
            </span>
          </div>


          <div className="dataset-stats">

            <div>
              <span>Rows</span>

              <strong>
                {dataset.profile.rows}
              </strong>
            </div>


            <div>
              <span>Columns</span>

              <strong>
                {dataset.profile.columns}
              </strong>
            </div>

          </div>


          <div className="column-section">

            <h4>
              COLUMN INFORMATION
            </h4>


            <div className="column-information">

              {dataset.profile.column_names.map(
                (column) => (

                  <div
                    key={column}
                    className="column-row"
                  >

                    <span className="column-name">
                      {column}
                    </span>

                    <span className="column-type">
                      {getColumnType(column)}
                    </span>

                  </div>

                )
              )}

            </div>

          </div>


          <div className="column-section">

            <h4>
              MISSING VALUES
            </h4>


            <div className="column-information">

              {Object.entries(
                dataset.profile.missing_values
              ).map(
                ([column, count]) => (

                  <div
                    key={column}
                    className="column-row"
                  >

                    <span className="column-name">
                      {column}
                    </span>

                    <span
                      className={
                        count === 0
                          ? "missing-zero"
                          : "missing-count"
                      }
                    >
                      {count}
                    </span>

                  </div>

                )
              )}

            </div>

          </div>


          <div className="column-section">

            <h4>
              COLUMN CATEGORIES
            </h4>


            <div className="category-summary">

              <div className="category-card">

                <span>
                  Numerical
                </span>

                <strong>
                  {
                    dataset.profile
                      .numerical_columns
                      .length
                  }
                </strong>

              </div>


              <div className="category-card">

                <span>
                  Categorical
                </span>

                <strong>
                  {
                    dataset.profile
                      .categorical_columns
                      .length
                  }
                </strong>

              </div>

            </div>

          </div>

        </div>

      )}


      {!dataset && (

        <div className="dataset-empty">

          <h3>
            No dataset uploaded
          </h3>

          <p>
            Upload a dataset to start
            asking questions.
          </p>

        </div>

      )}

    </aside>
  );
}


export default DatasetPanel;