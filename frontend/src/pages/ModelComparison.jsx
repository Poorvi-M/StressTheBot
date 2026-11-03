
function ModelComparison({ experimentResults }) {
  if (!experimentResults) {
    return (
      <div className="page-content">
        <div className="eyebrow">WORKSPACE / MODEL COMPARISON</div>
        <h1>Model Comparison</h1>
        <div className="empty-state">
          <h3>No experiment data available</h3>
          <p>Run an experiment to view model evaluation results.</p>
        </div>
      </div>
    );
  }

  const batchResults =
    experimentResults.batch_execution?.results ?? [];

  const riskRecords =
    experimentResults.risk_mapping?.risk_records ?? [];

  const models = {};

  batchResults.forEach((scenario) => {
    const responses = scenario.evaluation?.responses ?? [];

    responses.forEach((response) => {
      const key = `${response.provider}/${response.model}`;

      if (!models[key]) {
        models[key] = {
          provider: response.provider,
          model: response.model,
          successful: 0,
          errors: 0,
        };
      }

      if (response.status === "success") {
        models[key].successful += 1;
      } else {
        models[key].errors += 1;
      }
    });
  });

  riskRecords.forEach((record) => {
    const key = `${record.provider}/${record.model}`;

    if (!models[key]) {
      models[key] = {
        provider: record.provider,
        model: record.model,
        successful: 0,
        errors: 0,
      };
    }
  });

  const modelList = Object.entries(models).map(([key, model]) => {
    const findings = riskRecords.filter(
      (record) =>
        `${record.provider}/${record.model}` === key
    );

    return {
      ...model,
      findings: findings.length,
      potentialViolations: findings.filter(
        (record) => record.status === "potential_violation"
      ).length,
      missingExpected: findings.filter(
        (record) => record.status === "missing_expected_behavior"
      ).length,
      noDetectedIssue: findings.filter(
        (record) => record.status === "no_detected_issue"
      ).length,
      humanReview: findings.filter(
        (record) => record.requires_human_review
      ).length,
    };
  });

  return (
    <div className="page-content">
      <div className="page-heading">
        <div>
          <div className="eyebrow">WORKSPACE / MODEL COMPARISON</div>
          <h1>Model Comparison</h1>
          <p>
            Compare actual model execution and evaluation outcomes.
          </p>
        </div>
      </div>

      {experimentResults.research_only && (
        <div className="notice-panel experiment-warning">
          <span className="notice-icon">!</span>
          <div>
            <strong>Research-only results</strong>
            <p>These results are preliminary and require human review.</p>
          </div>
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-top">Models Evaluated</div>
          <div className="stat-value">{modelList.length}</div>
        </div>

        <div className="stat-card">
          <div className="stat-top">Successful Responses</div>
          <div className="stat-value">
            {modelList.reduce((sum, model) => sum + model.successful, 0)}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-top">API Errors</div>
          <div className="stat-value">
            {modelList.reduce((sum, model) => sum + model.errors, 0)}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-top">Potential Violations</div>
          <div className="stat-value">
            {modelList.reduce(
              (sum, model) => sum + model.potentialViolations,
              0
            )}
          </div>
        </div>
      </div>

      {modelList.length === 0 ? (
        <div className="empty-state">
          No model response records were returned by the experiment.
        </div>
      ) : (
        <>
          {modelList.length === 1 && (
            <div className="notice-panel">
              <span className="notice-icon">i</span>
              <div>
                <strong>Only one model has been evaluated</strong>
                <p>
                  A comparative ranking requires at least two models.
                  Run the same experiment with another configured provider
                  to enable a meaningful comparison.
                </p>
              </div>
            </div>
          )}

          <div className="rules-container">
            <div className="rules-table-heading">
              <div>
                <h2>Model Performance</h2>
                <p>Metrics calculated from actual experiment records.</p>
              </div>
            </div>

            <div className="table-wrapper">
              <table className="rules-table">
                <thead>
                  <tr>
                    <th>MODEL</th>
                    <th>SUCCESSFUL</th>
                    <th>API ERRORS</th>
                    <th>RISK RECORDS</th>
                    <th>POTENTIAL VIOLATIONS</th>
                    <th>MISSING BEHAVIOUR</th>
                  </tr>
                </thead>

                <tbody>
                  {modelList.map((model) => (
                    <tr key={`${model.provider}/${model.model}`}>
                      <td>
                        <div className="rule-title">{model.model}</div>
                        <div className="rule-id">{model.provider}</div>
                      </td>

                      <td>{model.successful}</td>
                      <td>{model.errors}</td>
                      <td>{model.findings}</td>
                      <td>{model.potentialViolations}</td>
                      <td>{model.missingExpected}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rules-container">
            <div className="rules-table-heading">
              <div>
                <h2>Evaluation Breakdown</h2>
                <p>Outcome distribution for each evaluated model.</p>
              </div>
            </div>

            {modelList.map((model) => (
              <div
                className="result-record"
                key={`${model.provider}-${model.model}`}
              >
                <strong>{model.model}</strong>

                <div className="summary-row">
                  <span>No detected issue</span>
                  <strong>{model.noDetectedIssue}</strong>
                </div>

                <div className="summary-row">
                  <span>Potential violations</span>
                  <strong>{model.potentialViolations}</strong>
                </div>

                <div className="summary-row">
                  <span>Missing expected behaviour</span>
                  <strong>{model.missingExpected}</strong>
                </div>

                <div className="summary-row">
                  <span>Requires human review</span>
                  <strong>{model.humanReview}</strong>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <div className="notice-panel">
        <span className="notice-icon">i</span>
        <div>
          <strong>Comparison limitation</strong>
          <p>
            Model outcomes depend on the scenarios and evaluation
            patterns used. A lower number of detected issues does not
            establish that a model is clinically safer.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ModelComparison;
