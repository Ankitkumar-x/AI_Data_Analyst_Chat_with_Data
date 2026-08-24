import { useState } from "react";

import Header from "./components/Header";
import DatasetPanel from "./components/DatasetPanel";
import ChatPanel from "./components/ChatPanel";
import AnalyticsDashboard from "./components/dashboard/AnalyticsDashboard";

import "./App.css";


function App() {

  const [dataset, setDataset] = useState(null);

  return (
    <div className="app">

      <Header />

      <main className="app-main">

        {dataset && (
          <AnalyticsDashboard
            dataset={dataset}
          />
        )}

        {!dataset && (
          <section className="dashboard-empty">
            <div className="dashboard-empty-icon">
              📊
            </div>

            <h2>
              Upload a dataset to begin
            </h2>

            <p>
              Your analytics dashboard will appear here
              after you upload a CSV or Excel file.
            </p>
          </section>
        )}

        <section className="ai-copilot-section">

          <div className="ai-copilot-header">

            <div>
              <span className="section-eyebrow">
                AI ANALYST
              </span>

              <h2>
                Your Data Copilot
              </h2>

              <p>
                Ask questions, explore insights, and analyze
                your dataset using natural language.
              </p>
            </div>

            <div className="ai-copilot-status">
              <span className="ai-status-dot"></span>
              AI Ready
            </div>

          </div>


          <div className="ai-workspace">

            <DatasetPanel
              onDatasetLoaded={setDataset}
            />

            <div className="ai-chat-card">
              <ChatPanel />
            </div>

          </div>

        </section>

      </main>

    </div>
  );
}


export default App;