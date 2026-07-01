import React, { useEffect, useState } from "react";
import {
  FaLayerGroup,
  FaCube,
  FaServer,
  FaDatabase,
  FaCode,
  FaBoxes
} from "react-icons/fa";

export default function ArchitectureLayers() {
  const [layers, setLayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/layers")
      .then((res) => res.json())
      .then((data) => {
        const safeLayers = Array.isArray(data.layers)
          ? data.layers
          : [];

        setLayers(safeLayers);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load architecture layers");
        setLoading(false);
      });
  }, []);

  const getLayerIcon = (layerName) => {
    const name = layerName?.toLowerCase() || "";

    if (name.includes("api")) return <FaServer />;
    if (name.includes("database")) return <FaDatabase />;
    if (name.includes("service")) return <FaCode />;
    if (name.includes("model")) return <FaCube />;

    return <FaLayerGroup />;
  };

  /*
  =====================================================
  LOADING
  =====================================================
  */

  if (loading) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #334155",
          borderRadius: "20px",
          padding: "50px",
          textAlign: "center",
          color: "#94a3b8"
        }}
      >
        <FaLayerGroup
          size={50}
          color="#38bdf8"
          style={{ marginBottom: "20px" }}
        />

        <h2>Loading Architecture Layers...</h2>
      </div>
    );
  }

  /*
  =====================================================
  ERROR
  =====================================================
  */

  if (error) {
    return (
      <div
        style={{
          background: "#111827",
          border: "1px solid #ef4444",
          borderRadius: "20px",
          padding: "40px",
          color: "#ef4444",
          textAlign: "center"
        }}
      >
        <h2>{error}</h2>
      </div>
    );
  }

  const totalComponents = layers.reduce(
    (sum, layer) =>
      sum +
      (layer.size ??
        layer.components?.length ??
        0),
    0
  );

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
          Architecture Layers
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px"
          }}
        >
          Layered view of repository architecture
        </p>
      </div>

      {/* SUMMARY */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(240px,1fr))",
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
              color: "#38bdf8",
              fontSize: "14px"
            }}
          >
            TOTAL LAYERS
          </div>

          <div
            style={{
              fontSize: "42px",
              fontWeight: "700",
              color: "#38bdf8"
            }}
          >
            {layers.length}
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
              color: "#22c55e",
              fontSize: "14px"
            }}
          >
            TOTAL COMPONENTS
          </div>

          <div
            style={{
              fontSize: "42px",
              fontWeight: "700",
              color: "#22c55e"
            }}
          >
            {totalComponents}
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
              color: "#a855f7",
              fontSize: "14px"
            }}
          >
            AVERAGE SIZE
          </div>

          <div
            style={{
              fontSize: "42px",
              fontWeight: "700",
              color: "#a855f7"
            }}
          >
            {layers.length
              ? Math.round(
                  totalComponents / layers.length
                )
              : 0}
          </div>
        </div>
      </div>

      {/* LAYERS */}

      <div
        style={{
          display: "grid",
          gap: "25px"
        }}
      >
        {layers.map((layer, index) => {
          const count =
            layer.size ??
            layer.components?.length ??
            0;

          return (
            <div
              key={layer.layer || index}
              style={{
                background: "#111827",
                border: "1px solid #334155",
                borderRadius: "20px",
                padding: "30px"
              }}
            >
              {/* TOP */}

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  alignItems: "center",
                  marginBottom: "25px"
                }}
              >
                <div
                  style={{
                    display: "flex",
                    gap: "15px",
                    alignItems: "center"
                  }}
                >
                  <div
                    style={{
                      width: "50px",
                      height: "50px",
                      borderRadius: "14px",
                      background:
                        "rgba(56,189,248,0.15)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "#38bdf8",
                      fontSize: "22px"
                    }}
                  >
                    {getLayerIcon(
                      layer.layer
                    )}
                  </div>

                  <div>
                    <h2
                      style={{
                        margin: 0,
                        color: "#38bdf8"
                      }}
                    >
                      {layer.layer ||
                        "Unknown Layer"}
                    </h2>

                    <div
                      style={{
                        color: "#94a3b8"
                      }}
                    >
                      {count} components
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
                      "#0f172a",
                    border:
                      "1px solid #334155",
                    color: "#cbd5e1"
                  }}
                >
                  Layer #{index + 1}
                </div>
              </div>

              {/* COMPONENTS */}

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "12px"
                }}
              >
                {(Array.isArray(
                  layer.components
                )
                  ? layer.components
                  : []
                )
                  .slice(0, 40)
                  .map(
                    (
                      component,
                      idx
                    ) => {
                      const name =
                        typeof component ===
                        "string"
                          ? component
                          : component?.name ||
                            JSON.stringify(
                              component
                            );

                      return (
                        <div
                          key={
                            name + idx
                          }
                          style={{
                            background:
                              "#0f172a",
                            border:
                              "1px solid #334155",
                            borderRadius:
                              "10px",
                            padding:
                              "8px 14px",
                            color:
                              "#cbd5e1",
                            fontSize:
                              "13px",
                            display:
                              "flex",
                            alignItems:
                              "center",
                            gap: "8px"
                          }}
                        >
                          <FaBoxes
                            color="#38bdf8"
                            size={12}
                          />

                          {name}
                        </div>
                      );
                    }
                  )}

                {count > 40 && (
                  <div
                    style={{
                      padding:
                        "8px 14px",
                      background:
                        "#1e293b",
                      borderRadius:
                        "10px",
                      color:
                        "#94a3b8"
                    }}
                  >
                    +{count - 40} more
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}