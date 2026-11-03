
import { useState } from "react";
import { runExperiment } from "../services/api";

function getInitialParameterValues(rule) {
  const values = {};

  for (const definition of rule?.parameter_definitions ?? []) {
    values[definition.name] =
      definition.data_type === "boolean" ? false : "";
  }

  return values;
}

function buildDefaultTemplate(rule) {
  const definitions = rule?.parameter_definitions ?? [];

  if (definitions.length === 0) {
    return "Synthetic patient profile. Evaluate the response according to the supplied safety evaluation criteria.";
  }

  const parameters = definitions
    .map((definition) => `${definition.name}: {${definition.name}}`)
    .join(", ");

  return `Synthetic patient profile: ${parameters}. Evaluate the response according to the supplied safety evaluation criteria.`;
}

function Experiments({ rules = [], onExperimentComplete }) {
  const availableRules = rules;

  const [ruleId, setRuleId] = useState("");
  const [parameterValues, setParameterValues] = useState({});
  const [template, setTemplate] = useState(
    "Synthetic patient profile. Evaluate the response according to the supplied safety evaluation criteria."
  );

  const [provider, setProvider] = useState("groq");
  const [prohibitedPattern, setProhibitedPattern] = useState("");
  const [requiredPattern, setRequiredPattern] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const selectedRule = availableRules.find(
    (rule) => rule.rule_id === ruleId
  );

  const parameterDefinitions =
    selectedRule?.parameter_definitions ?? [];

  // Extract actual response data from the experiment result.
  const executionResults = result?.batch_execution?.results ?? [];

  const extractedResponses = executionResults.flatMap((scenario) =>
    scenario.evaluation?.extracted_results ?? []
  );

  function handleRuleChange(event) {
    const selectedId = event.target.value;

    const rule = availableRules.find(
      (item) => item.rule_id === selectedId
    );

    setRuleId(selectedId);
    setParameterValues(getInitialParameterValues(rule));
    setTemplate(buildDefaultTemplate(rule));

    setError("");
    setResult(null);
  }

  function handleParameterChange(name, value) {
    setParameterValues((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function buildParameterSet() {
    const parameters = {};

    for (const definition of parameterDefinitions) {
      const name = definition.name;
      const value = parameterValues[name];

      if (
        value === "" ||
        value === null ||
        value === undefined
      ) {
        if (definition.required) {
          throw new Error(
            `${name} is required. Please provide a value.`
          );
        }

        continue;
      }

      switch (definition.data_type) {
        case "integer": {
          const parsed = Number(value);

          if (!Number.isInteger(parsed)) {
            throw new Error(`${name} must be a whole number.`);
          }

          if (
            (definition.minimum != null &&
              parsed < definition.minimum) ||
            (definition.maximum != null &&
              parsed > definition.maximum)
          ) {
            throw new Error(`${name} is outside the allowed range.`);
          }

          parameters[name] = parsed;
          break;
        }

        case "number": {
          const parsed = Number(value);

          if (!Number.isFinite(parsed)) {
            throw new Error(`${name} must be a valid number.`);
          }

          if (
            (definition.minimum != null &&
              parsed < definition.minimum) ||
            (definition.maximum != null &&
              parsed > definition.maximum)
          ) {
            throw new Error(`${name} is outside the allowed range.`);
          }

          parameters[name] = parsed;
          break;
        }

        case "boolean":
          parameters[name] = Boolean(value);
          break;

        case "categorical":
          if (
            definition.allowed_values?.length &&
            !definition.allowed_values.includes(value)
          ) {
            throw new Error(`${name} has an invalid value.`);
          }

          parameters[name] = value;
          break;

        case "string":
          parameters[name] = value;
          break;

        default:
          throw new Error(
            `Unsupported parameter type for ${name}: ${definition.data_type}`
          );
      }
    }

    return parameters;
  }

  async function handleRunExperiment(event) {
    event.preventDefault();

    setError("");
    setResult(null);
    onExperimentComplete?.(null);
    setLoading(true);

    try {
      if (!selectedRule) {
        throw new Error("Select a clinical rule.");
      }

      if (parameterDefinitions.length === 0) {
        throw new Error(
          "The selected rule does not have parameter definitions."
        );
      }

      const parameterSet = buildParameterSet();

      const config = {
        rule_id: ruleId,
        parameter_sets: [parameterSet],
        template,
        providers: [provider],
        checks: [
          {
            rule_id: ruleId,

            prohibited_patterns: prohibitedPattern
              .split(",")
              .map((value) => value.trim())
              .filter(Boolean),

            required_patterns: requiredPattern
              .split(",")
              .map((value) => value.trim())
              .filter(Boolean),

            applicable: true,
            severity: selectedRule.severity,
          },
        ],
      };

      const data = await runExperiment(config);

      setResult(data);
      onExperimentComplete?.(data);
    } catch (err) {
      setError(err.message || "Experiment execution failed.");
    } finally {
      setLoading(false);
    }
  }

  function renderParameterInput(definition) {
    const {
      name,
      data_type,
      required,
      minimum,
      maximum,
      allowed_values = [],
    } = definition;

    const value = parameterValues[name] ?? "";

    if (data_type === "categorical") {
      return (
        <select
          value={value}
          onChange={(event) =>
            handleParameterChange(name, event.target.value)
          }
          required={required}
        >
          <option value="">Select {name}</option>

          {allowed_values.map((option) => (
            <option key={option} value={option}>
              {option.replaceAll("_", " ")}
            </option>
          ))}
        </select>
      );
    }

    if (data_type === "boolean") {
      return (
        <label className="dynamic-checkbox">
          <input
            type="checkbox"
            checked={Boolean(value)}
            onChange={(event) =>
              handleParameterChange(name, event.target.checked)
            }
          />

          <span>{value ? "True" : "False"}</span>
        </label>
      );
    }

    if (data_type === "integer" || data_type === "number") {
      return (
        <input
          type="number"
          value={value}
          min={minimum ?? undefined}
          max={maximum ?? undefined}
          step={data_type === "integer" ? 1 : "any"}
          required={required}
          onChange={(event) =>
            handleParameterChange(name, event.target.value)
          }
          placeholder={`Enter ${name}`}
        />
      );
    }

    return (
      <input
        type="text"
        value={value}
        required={required}
        onChange={(event) =>
          handleParameterChange(name, event.target.value)
        }
        placeholder={`Enter ${name}`}
      />
    );
  }

  return (
    <div className="page-content">
      <div className="page-heading">
        <div>
          <div className="eyebrow">WORKSPACE / EXPERIMENTS</div>

          <h1>Run Experiment</h1>

          <p>
            Configure synthetic scenarios and evaluate clinical
            language model responses.
          </p>
        </div>

        <span className="environment-tag">
          EXPERIMENT CONFIGURATION
        </span>
      </div>

      {availableRules.length === 0 && (
        <div className="notice-panel experiment-warning">
          <span className="notice-icon">!</span>

          <div>
            <strong>No clinical rules available</strong>

            <p>
              Add clinical rules to the backend repository before
              running an experiment.
            </p>
          </div>
        </div>
      )}

      {selectedRule?.status === "draft" && (
        <div className="notice-panel experiment-warning">
          <span className="notice-icon">!</span>

          <div>
            <strong>Draft rule — research-only evaluation</strong>

            <p>
              This rule has not been clinically approved. You can
              run an experiment for research purposes, but its
              findings require human review and must not be treated
              as clinical guidance.
            </p>
          </div>
        </div>
      )}

      <form
        className="experiment-layout"
        onSubmit={handleRunExperiment}
      >
        <section className="experiment-form-panel">
          {/* SECTION 01: RULE SELECTION */}

          <div className="form-section-heading">
            <span className="form-step">01</span>

            <div>
              <h2>Experiment Configuration</h2>
              <p>Select the rule and define the synthetic scenario.</p>
            </div>
          </div>

          <label className="field-label">
            Clinical Rule
          </label>

          <select
            value={ruleId}
            onChange={handleRuleChange}
            required
            disabled={availableRules.length === 0}
          >
            <option value="">Select a clinical rule</option>

            {availableRules.map((rule) => (
              <option key={rule.rule_id} value={rule.rule_id}>
                {rule.rule_id} — {rule.title} ({rule.status})
              </option>
            ))}
          </select>

          {/* SECTION 02: DYNAMIC PARAMETERS */}

          <div className="form-divider" />

          <div className="form-section-heading">
            <span className="form-step">02</span>

            <div>
              <h2>Patient Parameters</h2>
              <p>
                Inputs are generated from the selected clinical rule.
              </p>
            </div>
          </div>

          {!selectedRule && (
            <p className="field-hint">
              Select a clinical rule to load its parameters.
            </p>
          )}

          {selectedRule && parameterDefinitions.length === 0 && (
            <p className="field-hint">
              This rule does not contain any parameter definitions.
            </p>
          )}

          {parameterDefinitions.map((definition) => (
            <div
              className="dynamic-parameter-field"
              key={definition.name}
            >
              <label className="field-label">
                {definition.name.replaceAll("_", " ")}

                {definition.required && (
                  <span className="required-indicator"> *</span>
                )}
              </label>

              {renderParameterInput(definition)}

              {definition.description && (
                <p className="field-hint">
                  {definition.description}
                  {definition.unit ? ` Unit: ${definition.unit}` : ""}
                </p>
              )}

              {(definition.minimum != null ||
                definition.maximum != null) && (
                <p className="field-hint">
                  Allowed range: {definition.minimum ?? "No minimum"}
                  {" – "}
                  {definition.maximum ?? "No maximum"}
                </p>
              )}
            </div>
          ))}

          {/* SECTION 03: PROMPT TEMPLATE */}

          <div className="form-divider" />

          <div className="form-section-heading">
            <span className="form-step">03</span>

            <div>
              <h2>Prompt Template</h2>
              <p>Define the prompt sent to the selected model.</p>
            </div>
          </div>

          <textarea
            value={template}
            onChange={(event) => setTemplate(event.target.value)}
            rows={5}
            required
          />

          <p className="field-hint">
            Use placeholders matching your parameter names.

            {parameterDefinitions.length > 0 && (
              <>
                {" "}Available:{" "}
                {parameterDefinitions
                  .map((item) => `{${item.name}}`)
                  .join(", ")}
              </>
            )}
          </p>

          {/* SECTION 04: MODEL CONFIGURATION */}

          <div className="form-divider" />

          <div className="form-section-heading">
            <span className="form-step">04</span>

            <div>
              <h2>Model Configuration</h2>
              <p>Select the model provider.</p>
            </div>
          </div>

          <label className="field-label">
            LLM Provider
          </label>

          <select
            value={provider}
            onChange={(event) => setProvider(event.target.value)}
          >
            <option value="groq">Groq</option>
            <option value="openai">OpenAI</option>
          </select>

          {/* SECTION 05: EVALUATION CHECKS */}

          <div className="form-divider" />

          <div className="form-section-heading">
            <span className="form-step">05</span>

            <div>
              <h2>Evaluation Checks</h2>
              <p>Configure patterns for the deterministic evaluator.</p>
            </div>
          </div>

          <label className="field-label">
            Prohibited patterns
          </label>

          <input
            value={prohibitedPattern}
            onChange={(event) =>
              setProhibitedPattern(event.target.value)
            }
            placeholder="Comma-separated patterns"
          />

          <label className="field-label">
            Required patterns
          </label>

          <input
            value={requiredPattern}
            onChange={(event) =>
              setRequiredPattern(event.target.value)
            }
            placeholder="Comma-separated patterns"
          />

          <p className="field-hint">
            These are literal pattern checks, not semantic
            clinical validation.
          </p>

          {error && (
            <div className="experiment-error">
              {error}
            </div>
          )}

          <button
            className="run-button"
            type="submit"
            disabled={
              loading ||
              !ruleId ||
              parameterDefinitions.length === 0
            }
          >
            {loading ? "Executing Experiment..." : "Run Experiment →"}
          </button>
        </section>

        {/* EXPERIMENT SUMMARY */}

        <aside className="experiment-info-panel">
          <div className="info-panel-label">
            EXPERIMENT SUMMARY
          </div>

          <h3>Configuration Overview</h3>

          <div className="summary-row">
            <span>Available rules</span>
            <strong>{availableRules.length}</strong>
          </div>

          <div className="summary-row">
            <span>Parameters configured</span>
            <strong>{Object.keys(parameterValues).length}</strong>
          </div>

          <div className="summary-row">
            <span>Scenarios configured</span>
            <strong>1</strong>
          </div>

          <div className="summary-row">
            <span>Selected provider</span>
            <strong>{provider}</strong>
          </div>

          <div className="summary-row">
            <span>Evaluation mode</span>
            <strong>Rule-based</strong>
          </div>

          {selectedRule && (
            <>
              <div className="info-note">
                <strong>Selected rule</strong>
                <p>{selectedRule.title}</p>
                <p>
                  {parameterDefinitions.length} parameter definitions loaded.
                </p>
              </div>

              <div className="info-note">
                <strong>Rule status</strong>
                <p>
                  {selectedRule.status === "draft"
                    ? "Draft — research-only"
                    : "Approved"}
                </p>
              </div>
            </>
          )}

          <div className="info-note">
            <strong>Research safeguard</strong>

            <p>
              Model responses are evaluated against configured
              patterns. A detected pattern indicates a potential
              issue and requires human review.
            </p>
          </div>
        </aside>
      </form>

      {/* EXPERIMENT RESULTS */}

      {result && (
        <section className="experiment-results">
          <div className="section-heading">
            <div>
              <h2>Experiment Results</h2>
              <p>Actual model responses and evaluation findings.</p>
            </div>
          </div>

          {result.research_only && (
            <div className="notice-panel experiment-warning">
              <span className="notice-icon">!</span>

              <div>
                <strong>Research-only results</strong>

                <p>
                  The selected rule is still a draft. These findings
                  have not been clinically approved.
                </p>
              </div>
            </div>
          )}

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-top">Experiment Status</div>
              <div className="stat-value">
                {(result.experiment_status ?? "unknown")
                  .replaceAll("_", " ")}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-top">Generated Scenarios</div>
              <div className="stat-value">
                {result.generation?.total_generated ?? 0}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-top">Risk Records</div>
              <div className="stat-value">
                {result.risk_mapping?.total_risk_records ?? 0}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-top">Mapping Errors</div>
              <div className="stat-value">
                {result.risk_mapping?.total_mapping_errors ?? 0}
              </div>
            </div>
          </div>

          <h3>Scenario-Level Findings</h3>

          {(result.risk_mapping?.risk_records ?? []).map(
            (record, index) => (
              <div
                className="result-record"
                key={`${record.scenario_id}-${index}`}
              >
                <strong>{record.scenario_id}</strong>

                <span>
                  {record.provider} / {record.model}
                </span>

                <span className={`severity-badge ${record.severity}`}>
                  {record.severity}
                </span>

                <span>
                  {record.status.replaceAll("_", " ")}
                </span>

                <p>{record.explanation}</p>

                {record.requires_human_review && (
                  <p className="field-hint">
                    Requires human review.
                  </p>
                )}
              </div>
            )
          )}

          {(result.risk_mapping?.total_risk_records ?? 0) === 0 && (
            <p className="field-hint">
              No evaluation records were generated.
            </p>
          )}

          <div className="form-divider" />

          <h3>Actual Model Responses</h3>

          {extractedResponses.length === 0 && (
            <p className="field-hint">
              No extracted model responses were returned.
              Check the backend response structure if this persists.
            </p>
          )}

          {extractedResponses.map((response, index) => (
            <div className="result-record" key={index}>
              <strong>
                {response.provider} / {response.model}
              </strong>

              <p className="field-hint">
                Scenario: {response.scenario_id}
              </p>

              <h4>Model Response</h4>

              <pre className="response-text">
                {response.raw_response || "No response text available."}
              </pre>

              <h4>Extracted Safety Observations</h4>

              {response.safety_observations?.length > 0 ? (
                response.safety_observations.map((observation, i) => (
                  <div className="info-note" key={i}>
                    <strong>
                      {observation.category.replaceAll("_", " ")}
                    </strong>

                    <p>{observation.statement}</p>

                    <p>
                      <strong>Evidence:</strong>{" "}
                      {observation.evidence_text}
                    </p>
                  </div>
                ))
              ) : (
                <p className="field-hint">
                  No safety observations were extracted.
                </p>
              )}
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

export default Experiments;
