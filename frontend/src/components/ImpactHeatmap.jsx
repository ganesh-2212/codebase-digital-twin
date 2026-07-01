import { useEffect, useState } from "react";
import {
  FaFire,
  FaBolt,
  FaExclamationTriangle
} from "react-icons/fa";

export default function ImpactHeatmap() {
  const [components, setComponents] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetch(
      "http://localhost:8000/impact-heatmap"
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setComponents(
            data.components || []
          );
        }

        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const colorForRisk = (risk) => {
    if (risk === "critical")
      return "#ef4444";

    if (risk === "high")
      return "#f97316";

    if (risk === "medium")
      return "#eab308";

    return "#22c55e";
  };

  const labelForRisk = (risk) => {
    if (risk === "critical")
      return "Critical";

    if (risk === "high")
      return "High";

    if (risk === "medium")
      return "Medium";

    return "Low";
  };

  if (loading) {
    return (
      <div
        style={{
          background: "#111827",
          border:
            "1px solid #334155",
          borderRadius: "20px",
          padding: "60px",
          textAlign: "center",
          color: "#94a3b8"
        }}
      >
        Loading impact heatmap...
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
          Impact Heatmap
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px"
          }}
        >
          Components ranked by
          architectural blast radius
          and change impact.
        </p>
      </div>

      {/* SUMMARY */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(250px,1fr))",
          gap: "25px",
          marginBottom: "35px"
        }}
      >
        <div
          style={{
            background: "#111827",
            border:
              "1px solid #334155",
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
            ANALYZED COMPONENTS
          </div>

          <div
            style={{
              fontSize: "38px",
              fontWeight: "700",
              color: "#38bdf8"
            }}
          >
            {components.length}
          </div>
        </div>

        <div
          style={{
            background: "#111827",
            border:
              "1px solid #334155",
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
            CRITICAL COMPONENTS
          </div>

          <div
            style={{
              fontSize: "38px",
              fontWeight: "700",
              color: "#ef4444"
            }}
          >
            {
              components.filter(
                (c) =>
                  c.risk ===
                  "critical"
              ).length
            }
          </div>
        </div>

        <div
          style={{
            background: "#111827",
            border:
              "1px solid #334155",
            borderRadius: "18px",
            padding: "30px"
          }}
        >
          <div
            style={{
              color: "#22c55e",
              fontSize: "14px"
            }}
          >
            LOW RISK COMPONENTS
          </div>

          <div
            style={{
              fontSize: "38px",
              fontWeight: "700",
              color: "#22c55e"
            }}
          >
            {
              components.filter(
                (c) =>
                  c.risk ===
                  "low"
              ).length
            }
          </div>
        </div>
      </div>

      {/* HEATMAP */}

      <div
        style={{
          display: "grid",
          gap: "20px"
        }}
      >
        {components
          .slice(0, 30)
          .map((component) => (
            <div
              key={
                component.name
              }
              style={{
                background:
                  "#111827",
                border:
                  "1px solid #334155",
                borderRadius:
                  "18px",
                padding: "25px"
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
                    "20px"
                }}
              >
                <div>
                  <h3
                    style={{
                      margin: 0
                    }}
                  >
                    {
                      component.name
                    }
                  </h3>

                  <div
                    style={{
                      color:
                        "#94a3b8",
                      marginTop:
                        "6px"
                    }}
                  >
                    Impact score:
                    {" "}
                    {
                      component.impact_score
                    }
                  </div>
                </div>

                <div
                  style={{
                    padding:
                      "8px 18px",
                    borderRadius:
                      "999px",
                    background:
                      `${colorForRisk(
                        component.risk
                      )}22`,
                    color:
                      colorForRisk(
                        component.risk
                      ),
                    fontWeight:
                      "700"
                  }}
                >
                  {
                    labelForRisk(
                      component.risk
                    )
                  }
                </div>
              </div>

              {/* BAR */}

              <div
                style={{
                  height: "16px",
                  background:
                    "#0f172a",
                  borderRadius:
                    "999px",
                  overflow:
                    "hidden"
                }}
              >
                <div
                  style={{
                    width:
                      `${Math.min(
                        component.impact_score,
                        100
                      )}%`,
                    height:
                      "100%",
                    background:
                      colorForRisk(
                        component.risk
                      ),
                    borderRadius:
                      "999px",
                    transition:
                      "0.5s ease"
                  }}
                />
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}