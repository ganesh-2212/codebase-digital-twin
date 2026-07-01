import { useState } from "react";
import {
  FaBolt,
  FaProjectDiagram,
  FaExclamationTriangle,
  FaCodeBranch,
  FaRobot
} from "react-icons/fa";

export default function ImpactAnalysis() {
  const [component, setComponent] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const analyze = async () => {
    if (!component.trim()) return;

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/impact",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            component,
          }),
        }
      );

      const data =
        await response.json();

      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: "100%" }}>
      {/* HEADER */}

      <div
        style={{
          marginBottom: "35px",
        }}
      >
        <h1
          style={{
            fontSize: "42px",
            fontWeight: "800",
            marginBottom: "10px",
          }}
        >
          Impact Analysis
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px",
          }}
        >
          Estimate the blast radius of
          modifying a component in the
          repository architecture.
        </p>
      </div>

      {/* INPUT CARD */}

      <div
        style={{
          background: "#111827",
          border: "1px solid #334155",
          borderRadius: "20px",
          padding: "30px",
          marginBottom: "30px",
        }}
      >
        <div
          style={{
            display: "flex",
            gap: "15px",
            flexWrap: "wrap",
          }}
        >
          <input
            value={component}
            onChange={(e) =>
              setComponent(
                e.target.value
              )
            }
            placeholder="Enter component name..."
            style={{
              flex: 1,
              minWidth: "350px",
              padding: "16px",
              borderRadius: "12px",
              border:
                "1px solid #475569",
              background:
                "#1e293b",
              color: "white",
              fontSize: "16px",
              outline: "none",
            }}
          />

          <button
            onClick={analyze}
            disabled={loading}
            style={{
              padding:
                "16px 28px",
              borderRadius:
                "12px",
              border: "none",
              background:
                loading
                  ? "#475569"
                  : "#2563eb",
              color: "white",
              fontWeight:
                "700",
              cursor:
                "pointer",
              minWidth: "180px",
            }}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Impact"}
          </button>
        </div>
      </div>

      {/* RESULTS */}

      {result && (
        <>
          {/* METRICS */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(260px,1fr))",
              gap: "25px",
              marginBottom: "30px",
            }}
          >
            <div
              style={{
                background:
                  "#111827",
                border:
                  "1px solid #334155",
                borderRadius:
                  "18px",
                padding: "30px",
              }}
            >
              <div
                style={{
                  color:
                    "#38bdf8",
                  fontSize:
                    "14px",
                }}
              >
                IMPACT SCORE
              </div>

              <div
                style={{
                  fontSize:
                    "38px",
                  fontWeight:
                    "700",
                  color:
                    "#38bdf8",
                }}
              >
                {
                  result.impact_score ??
                  "-"
                }
              </div>
            </div>

            <div
              style={{
                background:
                  "#111827",
                border:
                  "1px solid #334155",
                borderRadius:
                  "18px",
                padding: "30px",
              }}
            >
              <div
                style={{
                  color:
                    "#f59e0b",
                  fontSize:
                    "14px",
                }}
              >
                AFFECTED FILES
              </div>

              <div
                style={{
                  fontSize:
                    "38px",
                  fontWeight:
                    "700",
                  color:
                    "#f59e0b",
                }}
              >
                {result.files
                  ?.length || 0}
              </div>
            </div>

            <div
              style={{
                background:
                  "#111827",
                border:
                  "1px solid #334155",
                borderRadius:
                  "18px",
                padding: "30px",
              }}
            >
              <div
                style={{
                  color:
                    "#a855f7",
                  fontSize:
                    "14px",
                }}
              >
                DEPENDENCIES
              </div>

              <div
                style={{
                  fontSize:
                    "38px",
                  fontWeight:
                    "700",
                  color:
                    "#a855f7",
                }}
              >
                {result.dependencies
                  ?.length || 0}
              </div>
            </div>
          </div>

          {/* DETAILS */}

          <div
            style={{
              background:
                "#111827",
              border:
                "1px solid #334155",
              borderRadius:
                "20px",
              padding: "35px",
            }}
          >
            <h2
              style={{
                marginBottom:
                  "25px",
              }}
            >
              Analysis Result
            </h2>

            <div
              style={{
                display: "grid",
                gap: "20px",
              }}
            >
              {Object.entries(
                result
              ).map(
                ([key, value]) => (
                  <div
                    key={key}
                    style={{
                      background:
                        "#0f172a",
                      border:
                        "1px solid #334155",
                      borderRadius:
                        "12px",
                      padding:
                        "18px",
                    }}
                  >
                    <div
                      style={{
                        color:
                          "#38bdf8",
                        marginBottom:
                          "10px",
                        fontWeight:
                          "600",
                        textTransform:
                          "uppercase",
                        fontSize:
                          "13px",
                      }}
                    >
                      {key}
                    </div>

                    <div
                      style={{
                        color:
                          "#cbd5e1",
                        whiteSpace:
                          "pre-wrap",
                        wordBreak:
                          "break-word",
                      }}
                    >
                      {typeof value ===
                      "object"
                        ? JSON.stringify(
                            value,
                            null,
                            2
                          )
                        : String(
                            value
                          )}
                    </div>
                  </div>
                )
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}