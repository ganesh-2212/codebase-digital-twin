import { useEffect, useState } from "react";
import {
  FaBug,
  FaExclamationTriangle,
  FaCheckCircle
} from "react-icons/fa";

export default function SmellDetection() {
  const [smells, setSmells] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/smells")
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setSmells(data.smells || []);
        }

        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const severityColor = (severity) => {
    const s = severity?.toLowerCase();

    if (s === "critical") return "#ef4444";
    if (s === "high") return "#f97316";
    if (s === "medium") return "#eab308";

    return "#22c55e";
  };

  return (
    <div>
      {/* Header */}

      <div
        style={{
          background: "#111827",
          border: "1px solid #334155",
          borderRadius: "16px",
          padding: "25px",
          marginBottom: "25px",
        }}
      >
        <h1
          style={{
            fontSize: "28px",
            marginBottom: "10px",
          }}
        >
          Software Smells
        </h1>

        <p
          style={{
            color: "#94a3b8",
          }}
        >
          Detect maintainability issues, architecture smells and
          code quality risks across the repository.
        </p>
      </div>

      {/* Loading */}

      {loading && (
        <div
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "16px",
            padding: "25px",
            color: "#94a3b8",
          }}
        >
          Loading software smells...
        </div>
      )}

      {/* Empty State */}

      {!loading && smells.length === 0 && (
        <div
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "16px",
            padding: "30px",
            textAlign: "center",
          }}
        >
          <FaCheckCircle
            size={45}
            color="#22c55e"
            style={{
              marginBottom: "15px",
            }}
          />

          <h2>No Software Smells Detected</h2>

          <p
            style={{
              color: "#94a3b8",
            }}
          >
            The repository appears healthy.
          </p>
        </div>
      )}

      {/* Smells */}

      <div
        style={{
          display: "grid",
          gap: "20px",
        }}
      >
        {smells.map((smell, index) => (
          <div
            key={smell.name || index}
            style={{
              background: "#111827",
              border: "1px solid #334155",
              borderRadius: "16px",
              padding: "25px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "18px",
                flexWrap: "wrap",
                gap: "10px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                }}
              >
                <FaBug
                  color={severityColor(smell.severity)}
                  size={22}
                />

                <div>
                  <h3
                    style={{
                      margin: 0,
                    }}
                  >
                    {smell.name}
                  </h3>

                  <div
                    style={{
                      color: "#94a3b8",
                      marginTop: "5px",
                      fontSize: "14px",
                    }}
                  >
                    {smell.type}
                  </div>
                </div>
              </div>

              <div
                style={{
                  background: severityColor(smell.severity),
                  padding: "6px 14px",
                  borderRadius: "999px",
                  fontSize: "13px",
                  fontWeight: "600",
                }}
              >
                {smell.severity}
              </div>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(160px,1fr))",
                gap: "15px",
              }}
            >
              <div
                style={{
                  background: "#0f172a",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                  padding: "15px",
                }}
              >
                <div
                  style={{
                    color: "#94a3b8",
                    fontSize: "13px",
                    marginBottom: "6px",
                  }}
                >
                  Smell Type
                </div>

                <div>{smell.type}</div>
              </div>

              <div
                style={{
                  background: "#0f172a",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                  padding: "15px",
                }}
              >
                <div
                  style={{
                    color: "#94a3b8",
                    fontSize: "13px",
                    marginBottom: "6px",
                  }}
                >
                  Severity
                </div>

                <div>{smell.severity}</div>
              </div>

              <div
                style={{
                  background: "#0f172a",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                  padding: "15px",
                }}
              >
                <div
                  style={{
                    color: "#94a3b8",
                    fontSize: "13px",
                    marginBottom: "6px",
                  }}
                >
                  Risk Score
                </div>

                <div>{smell.score}</div>
              </div>
            </div>

            {smell.description && (
              <div
                style={{
                  marginTop: "20px",
                  padding: "18px",
                  background: "#0f172a",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    marginBottom: "10px",
                    color: "#f59e0b",
                  }}
                >
                  <FaExclamationTriangle />
                  Description
                </div>

                <div
                  style={{
                    color: "#cbd5e1",
                    lineHeight: "1.7",
                  }}
                >
                  {smell.description}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}