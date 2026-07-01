import { useEffect, useState } from "react";

export default function ArchitectureHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/architecture-health")
      .then((res) => res.json())
      .then((data) => {
        setHealth(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #1e293b",
          borderRadius: "18px",
          padding: "50px",
          textAlign: "center",
          color: "#94a3b8",
        }}
      >
        <h2
          style={{
            color: "#38bdf8",
            marginBottom: "12px",
          }}
        >
          Loading Architecture Health...
        </h2>

        <p>Please wait while the architecture metrics are analyzed.</p>
      </div>
    );
  }

  if (!health) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #1e293b",
          borderRadius: "18px",
          padding: "50px",
          textAlign: "center",
          color: "#ef4444",
        }}
      >
        <h2>Unable to Load Architecture Health</h2>

        <p>Please make sure the backend server is running.</p>
      </div>
    );
  }

  const scoreColor =
    health.score >= 85
      ? "#22c55e"
      : health.score >= 70
      ? "#f59e0b"
      : "#ef4444";

  return (
    <div
      style={{
        background: "#111827",
        border: "1px solid #1e293b",
        borderRadius: "18px",
        padding: "30px",
        width: "100%",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "30px",
          flexWrap: "wrap",
          gap: "20px",
        }}
      >
        <div>
          <h2
            style={{
              margin: 0,
              color: "#38bdf8",
              fontSize: "28px",
            }}
          >
            Architecture Health
          </h2>

          <p
            style={{
              color: "#94a3b8",
              marginTop: "8px",
            }}
          >
            Overall software architecture quality score
          </p>
        </div>

        <div
          style={{
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontSize: "58px",
              fontWeight: "bold",
              color: scoreColor,
            }}
          >
            {health.score}
          </div>

          <div
            style={{
              color: scoreColor,
              fontWeight: "bold",
              fontSize: "18px",
            }}
          >
            {health.status}
          </div>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
          marginBottom: "35px",
        }}
      >
        <div
          style={{
            background: "#0f172a",
            padding: "20px",
            borderRadius: "14px",
            border: "1px solid #1e293b",
          }}
        >
          <h4
            style={{
              color: "#38bdf8",
              marginBottom: "12px",
            }}
          >
            Circular Dependencies
          </h4>

          <div
            style={{
              fontSize: "36px",
              fontWeight: "bold",
            }}
          >
            {health.breakdown?.circular_dependencies?.count ?? 0}
          </div>

          <div
            style={{
              color: "#ef4444",
              marginTop: "8px",
            }}
          >
            Penalty: -
            {health.breakdown?.circular_dependencies?.penalty ?? 0}
          </div>
        </div>

        <div
          style={{
            background: "#0f172a",
            padding: "20px",
            borderRadius: "14px",
            border: "1px solid #1e293b",
          }}
        >
          <h4
            style={{
              color: "#38bdf8",
              marginBottom: "12px",
            }}
          >
            Layer Violations
          </h4>

          <div
            style={{
              fontSize: "36px",
              fontWeight: "bold",
            }}
          >
            {health.breakdown?.layer_violations?.count ?? 0}
          </div>

          <div
            style={{
              color: "#ef4444",
              marginTop: "8px",
            }}
          >
            Penalty: -
            {health.breakdown?.layer_violations?.penalty ?? 0}
          </div>
        </div>

        <div
          style={{
            background: "#0f172a",
            padding: "20px",
            borderRadius: "14px",
            border: "1px solid #1e293b",
          }}
        >
          <h4
            style={{
              color: "#38bdf8",
              marginBottom: "12px",
            }}
          >
            Architecture Smells
          </h4>

          <div
            style={{
              fontSize: "36px",
              fontWeight: "bold",
            }}
          >
            {health.breakdown?.smells?.count ?? 0}
          </div>

          <div
            style={{
              color: "#ef4444",
              marginTop: "8px",
            }}
          >
            Penalty: -{health.breakdown?.smells?.penalty ?? 0}
          </div>
        </div>

        <div
          style={{
            background: "#0f172a",
            padding: "20px",
            borderRadius: "14px",
            border: "1px solid #1e293b",
          }}
        >
          <h4
            style={{
              color: "#38bdf8",
              marginBottom: "12px",
            }}
          >
            High Risk Components
          </h4>

          <div
            style={{
              fontSize: "36px",
              fontWeight: "bold",
            }}
          >
            {health.breakdown?.high_risk_components?.count ?? 0}
          </div>

          <div
            style={{
              color: "#ef4444",
              marginTop: "8px",
            }}
          >
            Penalty: -
            {health.breakdown?.high_risk_components?.penalty ?? 0}
          </div>
        </div>
      </div>

      <div
        style={{
          background: "#0f172a",
          border: "1px solid #1e293b",
          borderRadius: "14px",
          padding: "25px",
        }}
      >
        <h3
          style={{
            marginTop: 0,
            color: "#38bdf8",
            marginBottom: "20px",
          }}
        >
          Score Summary
        </h3>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "12px 0",
            borderBottom: "1px solid #1e293b",
          }}
        >
          <span>Base Score</span>
          <strong>100</strong>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "12px 0",
            borderBottom: "1px solid #1e293b",
          }}
        >
          <span>Total Penalty</span>
          <strong style={{ color: "#ef4444" }}>
            -
            {100 - health.score}
          </strong>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            paddingTop: "18px",
            fontSize: "22px",
            fontWeight: "bold",
          }}
        >
          <span>Final Architecture Score</span>

          <span style={{ color: scoreColor }}>
            {health.score}/100
          </span>
        </div>
      </div>
    </div>
  );
}