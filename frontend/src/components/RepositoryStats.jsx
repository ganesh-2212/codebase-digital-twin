import { useEffect, useState } from "react";

import {
  FaProjectDiagram,
  FaCube,
  FaLayerGroup,
  FaCodeBranch,
  FaRobot,
  FaNetworkWired,
} from "react-icons/fa";

export default function RepositoryStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/stats")
      .then((r) => r.json())
      .then(setStats);
  }, []);

  if (!stats) return null;

  const cardStyle = {
    background: "#111827",
    border: "1px solid #1e293b",
    borderRadius: "18px",
    padding: "22px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: "10px",
    transition: "0.25s",
    boxShadow: "0 8px 20px rgba(0,0,0,0.25)",
  };

  const valueStyle = {
    fontSize: "32px",
    fontWeight: "700",
    color: "#ffffff",
  };

  const titleStyle = {
    color: "#94a3b8",
    fontSize: "13px",
    textTransform: "uppercase",
    letterSpacing: "1px",
  };

  return (
    <div
      style={{
        marginTop: "30px",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          fontSize: "22px",
          fontWeight: "700",
        }}
      >
        Repository Metrics
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        <div style={cardStyle}>
          <FaProjectDiagram
            size={28}
            color="#38bdf8"
          />

          <div style={titleStyle}>
            Communities
          </div>

          <div style={valueStyle}>
            {stats.clusters || 0}
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            Architecture domains discovered
          </div>
        </div>

        <div style={cardStyle}>
          <FaCube
            size={28}
            color="#a855f7"
          />

          <div style={titleStyle}>
            Components
          </div>

          <div style={valueStyle}>
            {stats.components || 0}
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            Parsed code entities
          </div>
        </div>

        <div style={cardStyle}>
          <FaLayerGroup
            size={28}
            color="#22c55e"
          />

          <div style={titleStyle}>
            Layers
          </div>

          <div style={valueStyle}>
            {stats.layers || 0}
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            Architectural boundaries
          </div>
        </div>

        <div style={cardStyle}>
          <FaCodeBranch
            size={28}
            color="#f97316"
          />

          <div style={titleStyle}>
            Dependencies
          </div>

          <div style={valueStyle}>
            {stats.dependencies || 0}
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            Cross-component relations
          </div>
        </div>

        <div style={cardStyle}>
          <FaNetworkWired
            size={28}
            color="#eab308"
          />

          <div style={titleStyle}>
            Graph Nodes
          </div>

          <div style={valueStyle}>
            {stats.nodes || 0}
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            Dependency graph nodes
          </div>
        </div>

        <div style={cardStyle}>
          <FaRobot
            size={28}
            color="#06b6d4"
          />

          <div style={titleStyle}>
            AI Features
          </div>

          <div style={valueStyle}>
            8+
          </div>

          <div
            style={{
              color: "#64748b",
              fontSize: "13px",
            }}
          >
            GraphRAG intelligence modules
          </div>
        </div>
      </div>
    </div>
  );
}