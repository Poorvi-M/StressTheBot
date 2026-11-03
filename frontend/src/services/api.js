const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function fetchRules() {
  const response = await fetch(`${API_BASE_URL}/api/rules/`);

  if (!response.ok) {
    throw new Error(`Unable to fetch rules: ${response.status}`);
  }

  return response.json();
}

export async function runExperiment(experimentConfig) {
  const response = await fetch(
    `${API_BASE_URL}/api/experiments/run`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(experimentConfig),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Experiment execution failed"
    );
  }

  return data;
}