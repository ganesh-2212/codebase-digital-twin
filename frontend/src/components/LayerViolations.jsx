import { useEffect, useState } from "react";
import {
  FaExclamationTriangle,
  FaArrowRight,
  FaShieldAlt,
  FaBug
} from "react-icons/fa";

export default function LayerViolations() {
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchViolations = async () => {
      try {
        setLoading(true);

        const res = await fetch(
          "http://127.0.0.1:8000/layer-violations"
        );

        if (!res.ok) {
          throw new Error(
            "Failed to fetch layer violations"
          );
        }

        const data = await res.json();

        setViolations(
          data.violations || []
        );

        setError(null);
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load layer violations"
        );

        setViolations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchViolations();
  }, []);

  /*
  ==========================================
  LOADING STATE
  ==========================================
  */

  if (loading) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #334155",
          borderRadius: "20px",
          padding: "60px",
          textAlign: "center",
          color: "#94a3b8"
        }}
      >
        <FaExclamationTriangle
          size={50}
          color="#f59e0b"
          style={{
            marginBottom: "20px"
          }}
        />

        <h2>
          Loading Layer Violations...
        </h2>
      </div>
    );
  }

  /*
  ==========================================
  ERROR STATE
  ==========================================
  */

  if (error) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #ef4444",
          borderRadius: "20px",
          padding: "40px",
          textAlign: "center",
          color: "#ef4444"
        }}
      >
        <h2>{error}</h2>
      </div>
    );
  }

  return (
    <div style={{ width: "100%" }}>
      {/* HEADER */}

      <div
        style={{
          marginBottom: "35px"
        }}
      >
        <h1
          style={{
            fontSize: "42px",
            fontWeight: "800",
            marginBottom: "10px"
          }}
        >
          Layer Violations
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px"
          }}
        >
          Detect architectural rule breaks
          across application layers
        </p>
      </div>

      {/* SUMMARY CARDS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(260px,1fr))",
          gap: "25px",
          marginBottom: "35px"
        }}
      >
        <div
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "30px"
          }}
        >
          <div
            style={{
              color: "#ef4444",
              fontSize: "14px"
            }}
          >
            TOTAL VIOLATIONS
          </div>

          <div
            style={{
              fontSize: "42px",
              fontWeight: "700",
              color: "#ef4444"
            }}
          >
            {violations.length}
          </div>
        </div>

        <div
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "30px"
          }}
        >
          <div
            style={{
              color: "#f59e0b",
              fontSize: "14px"
            }}
          >
            ARCHITECTURE STATUS
          </div>

          <div
            style={{
              fontSize: "28px",
              fontWeight: "700",
              color:
                violations.length === 0
                  ? "#22c55e"
                  : "#f59e0b"
            }}
          >
            {violations.length === 0
              ? "Healthy"
              : "Needs Review"}
          </div>
        </div>

        <div
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "30px"
          }}
        >
          <div
            style={{
              color: "#38bdf8",
              fontSize: "14px"
            }}
          >
            LAYER INTEGRITY
          </div>

          <div
            style={{
              fontSize: "28px",
              fontWeight: "700",
              color:
                violations.length === 0
                  ? "#22c55e"
                  : "#ef4444"
            }}
          >
            {violations.length === 0
              ? "100%"
              : `${Math.max(
                  0,
                  100 -
                    violations.length *
                      5
                )}%`}
          </div>
        </div>
      </div>

      {/* EMPTY STATE */}

      {violations.length === 0 && (
        <div
          style={{
            background: "#111827",
            border: "1px solid #22c55e",
            borderRadius: "20px",
            padding: "60px",
            textAlign: "center"
          }}
        >
          <FaShieldAlt
            size={60}
            color="#22c55e"
            style={{
              marginBottom: "20px"
            }}
          />

          <h2
            style={{
              color: "#22c55e"
            }}
          >
            No Layer Violations Found
          </h2>

          <p
            style={{
              color: "#94a3b8"
            }}
          >
            Your architecture currently
            respects all defined layer
            boundaries.
          </p>
        </div>
      )}

      {/* VIOLATIONS */}

      <div
        style={{
          display: "grid",
          gap: "25px"
        }}
      >
        {violations.map(
          (
            violation,
            index
          ) => (
            <div
              key={index}
              style={{
                background:
                  "#111827",
                border:
                  "1px solid rgba(239,68,68,0.4)",
                borderRadius:
                  "20px",
                padding: "30px"
              }}
            >
              {/* TOP */}

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  alignItems:
                    "center",
                  marginBottom:
                    "25px"
                }}
              >
                <div
                  style={{
                    display: "flex",
                    gap: "15px",
                    alignItems:
                      "center"
                  }}
                >
                  <div
                    style={{
                      width: "55px",
                      height: "55px",
                      borderRadius:
                        "14px",
                      background:
                        "rgba(239,68,68,0.15)",
                      display:
                        "flex",
                      justifyContent:
                        "center",
                      alignItems:
                        "center",
                      color:
                        "#ef4444",
                      fontSize:
                        "24px"
                    }}
                  >
                    <FaBug />
                  </div>

                  <div>
                    <h2
                      style={{
                        margin: 0
                      }}
                    >
                      {violation.source ||
                        "Unknown Source"}
                    </h2>

                    <div
                      style={{
                        color:
                          "#94a3b8"
                      }}
                    >
                      Layer rule
                      violation
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    padding:
                      "8px 18px",
                    borderRadius:
                      "999px",
                    background:
                      "rgba(239,68,68,0.15)",
                    color:
                      "#ef4444",
                    fontWeight:
                      "600"
                  }}
                >
                  Critical
                </div>
              </div>

              {/* FLOW */}

              <div
                style={{
                  display: "flex",
                  alignItems:
                    "center",
                  gap: "20px",
                  marginBottom:
                    "25px",
                  flexWrap:
                    "wrap"
                }}
              >
                <div
                  style={{
                    padding:
                      "12px 20px",
                    background:
                      "#0f172a",
                    border:
                      "1px solid #334155",
                    borderRadius:
                      "12px"
                  }}
                >
                  {
                    violation.source_layer
                  }
                </div>

                <FaArrowRight color="#ef4444" />

                <div
                  style={{
                    padding:
                      "12px 20px",
                    background:
                      "#0f172a",
                    border:
                      "1px solid #334155",
                    borderRadius:
                      "12px"
                  }}
                >
                  {
                    violation.target_layer
                  }
                </div>
              </div>

              {/* TARGET */}

              <div
                style={{
                  background:
                    "#0f172a",
                  border:
                    "1px solid #334155",
                  borderRadius:
                    "12px",
                  padding:
                    "18px",
                  marginBottom:
                    "15px"
                }}
              >
                <div
                  style={{
                    color:
                      "#94a3b8",
                    fontSize:
                      "13px",
                    marginBottom:
                      "8px"
                  }}
                >
                  TARGET COMPONENT
                </div>

                <div>
                  {violation.target ||
                    "N/A"}
                </div>
              </div>

              {/* MESSAGE */}

              {violation.message && (
                <div
                  style={{
                    padding:
                      "18px",
                    borderRadius:
                      "12px",
                    background:
                      "rgba(239,68,68,0.08)",
                    border:
                      "1px solid rgba(239,68,68,0.25)",
                    color:
                      "#fca5a5"
                  }}
                >
                  {
                    violation.message
                  }
                </div>
              )}
            </div>
          )
        )}
      </div>
    </div>
  );
}