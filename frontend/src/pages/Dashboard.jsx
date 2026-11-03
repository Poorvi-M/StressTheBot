
function Dashboard({ rules, backendStatus, rulesLoading }) {
  const approvedRules = rules.filter(
    (rule) => rule.status === "approved"
  ).length;

  const draftRules = rules.filter(
    (rule) => rule.status === "draft"
  ).length;

  const backendConnected = backendStatus === "Connected";

  const stats = [
    {
      label: "Clinical Rules",
      value: rulesLoading ? "..." : rules.length,
      detail: "Rules loaded from backend",
      icon: "▤",
    },
    {
      label: "Approved Rules",
      value: rulesLoading ? "..." : approvedRules,
      detail: "Available for approved evaluation",
      icon: "✓",
    },
    {
      label: "Draft Rules",
      value: rulesLoading ? "..." : draftRules,
      detail: "Awaiting human review",
      icon: "◷",
    },
    {
      label: "Backend",
      value: backendStatus,
      detail: "API connectivity",
      icon: "⌁",
    },
  ];

  return (
    <div className="page-content">
      <div className="page-heading">
        <div>
          <div className="eyebrow">WORKSPACE / OVERVIEW</div>
          <h1>Dashboard</h1>
          <p>
            Monitor clinical AI safety evaluations and experiment activity.
          </p>
        </div>

        <div className="environment-tag">
          <span
            className={`status-dot ${
              backendConnected ? "online" : ""
            }`}
          />
          {backendConnected
            ? "BACKEND CONNECTED"
            : "BACKEND UNAVAILABLE"}
        </div>
      </div>

      <div className="welcome-panel">
        <div>
          <span className="panel-label">
            CLINICAL AI SAFETY TESTING
          </span>

          <h2>Push medical AI to its limits.</h2>

          <p>
            Stress-test clinical language models, identify potential
            safety failures, and map scenario-level risks.
          </p>
        </div>

        <div className="welcome-symbol">
          S<span>.</span>
        </div>
      </div>

      <div className="section-heading">
        <div>
          <h2>Platform Overview</h2>
          <p>Live information from your backend.</p>
        </div>
      </div>

      <div className="stats-grid">
        {stats.map((stat) => (
          <div className="stat-card" key={stat.label}>
            <div className="stat-top">
              <span>{stat.label}</span>
              <span className="stat-icon">{stat.icon}</span>
            </div>

            <div className="stat-value">{stat.value}</div>
            <div className="stat-detail">{stat.detail}</div>
          </div>
        ))}
      </div>

      <div className="section-heading">
        <div>
          <h2>Evaluation Pipeline</h2>
          <p>
            The stages used to evaluate clinical AI responses.
          </p>
        </div>
      </div>

      <div className="pipeline-grid">
        {[
          [
            "01",
            "Scenario Generation",
            "Create synthetic patient profiles",
          ],
          [
            "02",
            "Model Execution",
            "Query selected clinical LLMs",
          ],
          [
            "03",
            "Response Extraction",
            "Extract structured response facts",
          ],
          [
            "04",
            "Rule Evaluation",
            "Check configured safety constraints",
          ],
          [
            "05",
            "Risk Mapping",
            "Organize scenario-level findings",
          ],
        ].map(([number, title, description]) => (
          <div className="pipeline-card" key={number}>
            <span className="pipeline-number">{number}</span>
            <h3>{title}</h3>
            <p>{description}</p>
          </div>
        ))}
      </div>

      <div className="notice-panel">
        <span className="notice-icon">i</span>

        <div>
          <strong>Research evaluation only</strong>

          <p>
            StressTheBot is a clinical AI safety testing platform.
            Its findings are potential issues requiring human review,
            not medical diagnoses or treatment recommendations.
            Draft rules and their evaluation results are not
            clinically approved.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
