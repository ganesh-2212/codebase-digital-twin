import { useState } from "react";
import {
  FaExchangeAlt,
  FaExclamationTriangle,
  FaCheckCircle,
  FaBolt,
  FaRobot
} from "react-icons/fa";

export default function ChangePrediction() {
  const [component, setComponent] = useState("");

  const [prediction, setPrediction] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const predict = async () => {
    if (!component.trim()) return;

    try {
      setLoading(true);

      const response = await fetch(
        `http://localhost:8000/change-prediction/${component}`
      );

      const data =
        await response.json();

      setPrediction(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = () => {
    const risk =
      prediction?.risk?.toLowerCase() || "";

    if (
      risk.includes("high")
    )
      return "#ef4444";

    if (
      risk.includes("medium")
    )
      return "#f59e0b";

    return "#22c55e";
  };

  const getRiskLabel = () => {
    return (
      prediction?.risk ||
      "Unknown"
    );
  };

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
          Change Prediction
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px"
          }}
        >
          Predict blast radius and
          architectural impact of
          modifying a component
        </p>
      </div>

      {/* INPUT CARD */}

      <div
        style={{
          background: "#111827",
          border: "1px solid #334155",
          borderRadius: "20px",
          padding: "30px",
          marginBottom: "30px"
        }}
      >
        <div
          style={{
            display: "flex",
            gap: "15px",
            flexWrap: "wrap"
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
              outline: "none"
            }}
          />

          <button
            onClick={predict}
            disabled={
              loading
            }
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
              minWidth: "180px"
            }}
          >
            {loading
              ? "Predicting..."
              : "Predict Change"}
          </button>
        </div>
      </div>

      {/* RESULTS */}

      {prediction && (
        <>
          {/* SUMMARY */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(260px,1fr))",
              gap: "25px",
              marginBottom: "30px"
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
                padding: "30px"
              }}
            >
              <div
                style={{
                  color:
                    getRiskColor(),
                  fontSize:
                    "14px"
                }}
              >
                RISK LEVEL
              </div>

              <div
                style={{
                  fontSize:
                    "34px",
                  fontWeight:
                    "700",
                  color:
                    getRiskColor()
                }}
              >
                {getRiskLabel()}
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
                padding: "30px"
              }}
            >
              <div
                style={{
                  color:
                    "#38bdf8",
                  fontSize:
                    "14px"
                }}
              >
                IMPACT SCORE
              </div>

              <div
                style={{
                  fontSize:
                    "34px",
                  fontWeight:
                    "700",
                  color:
                    "#38bdf8"
                }}
              >
                {
                  prediction.impact
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
                padding: "30px"
              }}
            >
              <div
                style={{
                  color:
                    "#a855f7",
                  fontSize:
                    "14px"
                }}
              >
                AI ANALYSIS
              </div>

              <div
                style={{
                  fontSize:
                    "28px",
                  fontWeight:
                    "700",
                  color:
                    "#a855f7"
                }}
              >
                Ready
              </div>
            </div>
          </div>

          {/* MAIN CARD */}

          <div
            style={{
              background:
                "#111827",
              border:
                `1px solid ${getRiskColor()}55`,
              borderRadius:
                "20px",
              padding: "35px"
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems:
                  "center",
                gap: "20px",
                marginBottom:
                  "25px"
              }}
            >
              <div
                style={{
                  width: "60px",
                  height: "60px",
                  borderRadius:
                    "16px",
                  background:
                    `${getRiskColor()}22`,
                  display:
                    "flex",
                  justifyContent:
                    "center",
                  alignItems:
                    "center",
                  color:
                    getRiskColor(),
                  fontSize:
                    "28px"
                }}
              >
                <FaExchangeAlt />
              </div>

              <div>
                <h2
                  style={{
                    margin: 0
                  }}
                >
                  {component}
                </h2>

                <div
                  style={{
                    color:
                      "#94a3b8"
                  }}
                >
                  Change impact prediction
                </div>
              </div>
            </div>

            {/* IMPACT */}

            <div
              style={{
                marginBottom:
                  "25px"
              }}
            >
              <h3
                style={{
                  color:
                    "#38bdf8"
                }}
              >
                Estimated Impact
              </h3>

              <p
                style={{
                  color:
                    "#cbd5e1",
                  lineHeight:
                    "1.8"
                }}
              >
                {
                  prediction.impact
                }
              </p>
            </div>

            {/* REASON */}

            <div
              style={{
                background:
                  "#0f172a",
                border:
                  "1px solid #334155",
                borderRadius:
                  "14px",
                padding:
                  "25px"
              }}
            >
              <div
                style={{
                  display:
                    "flex",
                  gap: "10px",
                  alignItems:
                    "center",
                  marginBottom:
                    "15px",
                  color:
                    "#38bdf8"
                }}
              >
                <FaRobot />

                <strong>
                  AI Reasoning
                </strong>
              </div>

              <div
                style={{
                  color:
                    "#cbd5e1",
                  lineHeight:
                    "1.9"
                }}
              >
                {
                  prediction.reason
                }
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}