const navigation = [
  { id: "dashboard", label: "Overview", icon: "◫" },
  { id: "experiments", label: "Experiments", icon: "⌘" },
  { id: "rules", label: "Clinical Rules", icon: "▤" },
  { id: "risks", label: "Risk Analysis", icon: "◈" },
  { id: "models", label: "Model Comparison", icon: "⇄" },
];

function Sidebar({ activePage, setActivePage, backendStatus }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">S</div>

        <div>
          <h2>StressTheBot</h2>
          <p>CLINICAL AI EVALUATION</p>
        </div>
      </div>

      <div className="sidebar-section-label">WORKSPACE</div>

      <nav className="sidebar-nav">
        {navigation.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => setActivePage(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="connection-card">
          <div className="connection-heading">
            <span
              className={`status-dot ${
                backendStatus === "Connected" ? "online" : ""
              }`}
            />
            Backend
          </div>

          <p>{backendStatus}</p>
          <span className="connection-url">127.0.0.1:8000</span>
        </div>

        <div className="sidebar-footer">
          <span>STRESSTHEBOT</span>
          <span>RESEARCH BUILD 0.1</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;