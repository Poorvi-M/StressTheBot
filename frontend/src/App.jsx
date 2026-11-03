
import { useCallback, useEffect, useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Rules from "./pages/Rules";
import Experiments from "./pages/Experiments";
import RiskAnalysis from "./pages/RiskAnalysis";
import ModelComparison from "./pages/ModelComparison";

import {
  checkBackendHealth,
  fetchRules,
} from "./services/api";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [rules, setRules] = useState([]);
  const [rulesLoading, setRulesLoading] = useState(true);
  const [rulesError, setRulesError] = useState("");

  // Stores the latest experiment result for all pages.
  const [experimentResults, setExperimentResults] = useState(null);

  const loadBackendHealth = useCallback(async () => {
    try {
      const data = await checkBackendHealth();

      setBackendStatus(
        data.status === "healthy" ? "Connected" : "Unhealthy"
      );
    } catch {
      setBackendStatus("Disconnected");
    }
  }, []);

  const loadRules = useCallback(async () => {
    setRulesLoading(true);
    setRulesError("");

    try {
      const data = await fetchRules();
      setRules(data.rules || []);
    } catch (error) {
      setRulesError(error.message || "Unable to load rules.");
    } finally {
      setRulesLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBackendHealth();
    loadRules();
  }, [loadBackendHealth, loadRules]);

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return (
          <Dashboard
            rules={rules}
            backendStatus={backendStatus}
            rulesLoading={rulesLoading}
          />
        );

      case "rules":
        return (
          <Rules
            rules={rules}
            loading={rulesLoading}
            error={rulesError}
            refreshRules={loadRules}
          />
        );

      case "experiments":
        return (
          <Experiments
            rules={rules}
            onExperimentComplete={setExperimentResults}
          />
        );

      case "risks":
        return (
          <RiskAnalysis
            experimentResults={experimentResults}
          />
        );

      case "models":
        return (
          <ModelComparison
            experimentResults={experimentResults}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="app-shell">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        backendStatus={backendStatus}
      />

      <main className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <span className="topbar-label">
              RESEARCH WORKSPACE
            </span>

            <span className="topbar-divider">/</span>

            <span className="topbar-current">
              {activePage.replaceAll("_", " ")}
            </span>
          </div>

          <div className="topbar-right">
            <span
              className={`status-dot ${
                backendStatus === "Connected" ? "online" : ""
              }`}
            />

            <span>{backendStatus}</span>
          </div>
        </header>

        {renderPage()}

        <footer className="app-footer">
          <span>STRESSTHEBOT</span>
          <span>CLINICAL AI SAFETY EVALUATION PLATFORM</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
