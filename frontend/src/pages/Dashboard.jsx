import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [health, setHealth] = useState("...");
  const [violations, setViolations] = useState(0);
  const [smells, setSmells] = useState(0);
  const [cycles, setCycles] = useState(0);
  const [refactoring, setRefactoring] = useState(0);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/architecture-health")
      .then((res) =>
        setHealth(res.data.score?.toFixed(2) || "N/A")
      )
      .catch(() => setHealth("N/A"));

    axios
      .get("http://127.0.0.1:8000/layer-violations")
      .then((res) =>
        setViolations(res.data.count || 0)
      )
      .catch(() => setViolations(0));

    axios
      .get("http://127.0.0.1:8000/smells")
      .then((res) =>
        setSmells(res.data.count || 0)
      )
      .catch(() => setSmells(0));

    axios
      .get("http://127.0.0.1:8000/circular-dependencies")
      .then((res) =>
        setCycles(res.data.count || 0)
      )
      .catch(() => setCycles(0));

    axios
      .get("http://127.0.0.1:8000/refactoring-advice")
      .then((res) =>
        setRefactoring(res.data.count || 0)
      )
      .catch(() => setRefactoring(0));
  }, []);

  const cardStyle = {
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "14px",
    padding: "24px",
    minHeight: "170px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    transition: "all 0.2s ease",
  };

  const titleStyle = {
    fontSize: "17px",
    fontWeight: "600",
    color: "#e2e8f0",
    marginBottom: "10px",
  };

  const valueStyle = {
    fontSize: "46px",
    fontWeight: "700",
    lineHeight: "1",
  };

  const descriptionStyle = {
    color: "#94a3b8",
    fontSize: "14px",
    marginTop: "10px",
  };

  return (
    <div
      style={{
        width: "100%",
        color: "white",
      }}
    >
      {/* Header */}

      <div
        style={{
          marginBottom: "35px",
        }}
      >
        <h1
          style={{
            fontSize: "36px",
            fontWeight: "700",
            marginBottom: "8px",
          }}
        >
          Codebase Overview
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "15px",
          }}
        >
          Software architecture intelligence dashboard
        </p>
      </div>

      {/* Dashboard Cards */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "20px",
        }}
      >
        <div style={cardStyle}>
          <div style={titleStyle}>
            Architecture Health
          </div>

          <div
            style={{
              ...valueStyle,
              color: "#22c55e",
            }}
          >
            {health}
          </div>

          <div style={descriptionStyle}>
            Overall architecture quality score
          </div>
        </div>

        <div style={cardStyle}>
          <div style={titleStyle}>
            Layer Violations
          </div>

          <div
            style={{
              ...valueStyle,
              color: "#ef4444",
            }}
          >
            {violations}
          </div>

          <div style={descriptionStyle}>
            Broken architecture boundaries
          </div>
        </div>

        <div style={cardStyle}>
          <div style={titleStyle}>
            Architecture Smells
          </div>

          <div
            style={{
              ...valueStyle,
              color: "#facc15",
            }}
          >
            {smells}
          </div>

          <div style={descriptionStyle}>
            Maintainability issues detected
          </div>
        </div>

        <div style={cardStyle}>
          <div style={titleStyle}>
            Circular Dependencies
          </div>

          <div
            style={{
              ...valueStyle,
              color: "#38bdf8",
            }}
          >
            {cycles}
          </div>

          <div style={descriptionStyle}>
            Cyclic dependency chains
          </div>
        </div>

        <div style={cardStyle}>
          <div style={titleStyle}>
            Refactoring Suggestions
          </div>

          <div
            style={{
              ...valueStyle,
              color: "#a855f7",
            }}
          >
            {refactoring}
          </div>

          <div style={descriptionStyle}>
            AI-generated improvements
          </div>
        </div>

        <div style={cardStyle}>
          <div style={titleStyle}>
            AI Capabilities
          </div>

          <div
            style={{
              color: "#cbd5e1",
              lineHeight: "1.9",
              fontSize: "14px",
            }}
          >
            • GraphRAG Retrieval
            <br />
            • Impact Analysis
            <br />
            • Change Prediction
            <br />
            • Architecture Health
            <br />
            • Layer Detection
            <br />
            • Refactoring Advisor
          </div>
        </div>
      </div>
    </div>
  );
}