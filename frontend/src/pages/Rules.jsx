
function Rules({ rules, loading, error, refreshRules }) {
  const approvedCount = rules.filter(
    (rule) => rule.status === "approved"
  ).length;

  const draftCount = rules.filter(
    (rule) => rule.status === "draft"
  ).length;

  return (
    <div className="page-content">
      <div className="page-heading">
        <div>
          <div className="eyebrow">WORKSPACE / RULE LIBRARY</div>
          <h1>Clinical Rules</h1>
          <p>
            Browse sourced safety constraints used during model evaluation.
          </p>
        </div>

        <button className="secondary-button" onClick={refreshRules}>
          ↻ Refresh Rules
        </button>
      </div>

      <div className="rules-summary">
        <div>
          <span>TOTAL RULES</span>
          <strong>{loading ? "..." : rules.length}</strong>
        </div>

        <div>
          <span>APPROVED</span>
          <strong>{loading ? "..." : approvedCount}</strong>
        </div>

        <div>
          <span>DRAFT</span>
          <strong>{loading ? "..." : draftCount}</strong>
        </div>
      </div>

      <div className="rules-container">
        <div className="rules-table-heading">
          <div>
            <h2>Rule Repository</h2>
            <p>Rules retrieved from the FastAPI backend.</p>
          </div>

          <span className="live-label">LIVE DATA</span>
        </div>

        {loading && (
          <div className="empty-state">
            Loading clinical rules...
          </div>
        )}

        {error && (
          <div className="error-state">
            {error}
            <button onClick={refreshRules}>Try again</button>
          </div>
        )}

        {!loading && !error && rules.length === 0 && (
          <div className="empty-state">
            No clinical rules have been added yet.
          </div>
        )}

        {!loading && !error && rules.length > 0 && (
          <div className="table-wrapper">
            <table className="rules-table">
              <thead>
                <tr>
                  <th>RULE</th>
                  <th>CATEGORY</th>
                  <th>SEVERITY</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>
                {rules.map((rule) => (
                  <tr key={rule.rule_id}>
                    <td>
                      <div className="rule-title">{rule.title}</div>
                      <div className="rule-id">{rule.rule_id}</div>
                    </td>

                    <td>
                      {(rule.category || "uncategorized").replaceAll("_", " ")}
                    </td>

                    <td>
                      <span
                        className={`severity-badge ${rule.severity}`}
                      >
                        {rule.severity}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`rule-status ${rule.status}`}
                      >
                        {rule.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="notice-panel">
        <span className="notice-icon">i</span>

        <div>
          <strong>Research evaluation only</strong>
          <p>
            Draft rules can be used for research-only experiments.
            Their results are preliminary and require human review.
            Approved rules have undergone the required review process.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Rules;
