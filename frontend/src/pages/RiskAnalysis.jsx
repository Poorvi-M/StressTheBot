
function RiskAnalysis({ experimentResults }) {
  if (!experimentResults) {
    return (
      <div className="page-content">
        <div className="eyebrow">WORKSPACE / RISK ANALYSIS</div>
        <h1>Risk Analysis</h1>
        <div className="empty-state">
          <h3>No experiment data available</h3>
          <p>Run an experiment first to view scenario-level risk findings.</p>
        </div>
      </div>
    );
  }

  const mapping = experimentResults.risk_mapping ?? {};
  const records = mapping.risk_records ?? [];
  const summary = experimentResults.risk_summary ?? {};

  const statuses = [
    "potential_violation",
    "missing_expected_behavior",
    "no_detected_issue",
    "manual_review",
  ];

  const statusLabels = {
    potential_violation: "Potential violations",
    missing_expected_behavior: "Missing expected behavior",
    no_detected_issue: "No detected issue",
    manual_review: "Manual review",
  };

  const countStatus = (status) =>
    records.filter((record) => record.status === status).length;

  const severityCount = (severity) =>
    records.filter((record) => record.severity === severity).length;

  return (
    <div className="page-content">
      <div className="page-heading">
        <div>
          <div className="eyebrow">WORKSPACE / RISK ANALYSIS</div>
          <h1>Risk Analysis</h1>
          <p>
            Inspect scenario-level findings from actual model evaluations.
          </p>
        </div>
      </div>

      {experimentResults.research_only && (
        <div className="notice-panel experiment-warning">
          <span className="notice-icon">!</span>
          <div>
            <strong>Research-only evaluation</strong>
            <p>Findings are preliminary and require human review.</p>
          </div>
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-top">Total Risk Records</div>
          <div className="stat-value">{records.length}</div>
        </div>

        <div className="stat-card">
          <div className="stat-top">Potential Violations</div>
          <div className="stat-value">
            {countStatus("potential_violation")}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-top">Missing Expected Behaviour</div>
          <div className="stat-value">
            {countStatus("missing_expected_behavior")}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-top">Human Review Required</div>
          <div className="stat-value">
            {records.filter((record) => record.requires_human_review).length}
          </div>
        </div>
      </div>

      <div className="rules-container">
        <div className="rules-table-heading">
          <div>
            <h2>Severity Distribution</h2>
            <p>Based on the severity assigned to each evaluation record.</p>
          </div>
        </div>

        {["critical", "high", "medium", "low"].map((severity) => (
          <div className="summary-row" key={severity}>
            <span className={`severity-badge ${severity}`}>
              {severity}
            </span>
            <strong>{severityCount(severity)}</strong>
          </div>
        ))}
      </div>

      <div className="rules-container">
        <div className="rules-table-heading">
          <div>
            <h2>Evaluation Status</h2>
            <p>Classification of the evaluator's findings.</p>
          </div>
        </div>

        {statuses.map((status) => (
          <div className="summary-row" key={status}>
            <span>{statusLabels[status]}</span>
            <strong>{countStatus(status)}</strong>
          </div>
        ))}
      </div>

      <div className="rules-container">
        <div className="rules-table-heading">
          <div>
            <h2>Scenario-Level Risk Records</h2>
            <p>Detailed findings from the latest experiment.</p>
          </div>
        </div>

        {records.length === 0 ? (
          <div className="empty-state">No risk records were generated.</div>
        ) : (
          records.map((record, index) => (
            <div
              className="result-record"
              key={`${record.scenario_id}-${index}`}
            >
              <strong>{record.scenario_id}</strong>
              <span>{record.provider} / {record.model}</span>

              <span className={`severity-badge ${record.severity}`}>
                {record.severity}
              </span>

              <p>
                <strong>Status:</strong>{" "}
                {record.status.replaceAll("_", " ")}
              </p>

              <p>{record.explanation}</p>

              {record.matched_prohibited_patterns?.length > 0 && (
                <p>
                  <strong>Matched prohibited patterns:</strong>{" "}
                  {record.matched_prohibited_patterns.join(", ")}
                </p>
              )}

              {record.missing_required_patterns?.length > 0 && (
                <p>
                  <strong>Missing required patterns:</strong>{" "}
                  {record.missing_required_patterns.join(", ")}
                </p>
              )}

              {record.requires_human_review && (
                <p className="field-hint">Human review required.</p>
              )}
            </div>
          ))
        )}
      </div>

      <div className="notice-panel">
        <span className="notice-icon">i</span>
        <div>
          <strong>Interpretation limitation</strong>
          <p>
            These findings reflect deterministic pattern evaluation.
            They are not a definitive clinical safety assessment.
          </p>
        </div>
      </div>
    </div>
  );
}

export default RiskAnalysis;
