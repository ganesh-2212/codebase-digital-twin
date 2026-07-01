import React, { useEffect, useState } from "react";
import {
  FaUsers,
  FaProjectDiagram,
  FaChevronDown,
  FaLayerGroup,
} from "react-icons/fa";

export default function ArchitectureClusters() {
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/clusters")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setClusters(data);
        } else {
          setError(
            data.error ||
              "Invalid cluster response from backend"
          );
        }

        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const totalComponents = clusters.reduce(
    (sum, cluster) => sum + cluster.size,
    0
  );

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
          marginBottom: "30px",
        }}
      >
        <h1
          style={{
            fontSize: "42px",
            fontWeight: "800",
            marginBottom: "10px",
          }}
        >
          Architecture Communities
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "16px",
          }}
        >
          Community detection and modular architecture analysis
        </p>
      </div>

      {/* Statistics */}

      {!loading && !error && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "20px",
            marginBottom: "30px",
          }}
        >
          <div
            style={{
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "18px",
              padding: "25px",
            }}
          >
            <div
              style={{
                color: "#38bdf8",
                fontSize: "15px",
                marginBottom: "10px",
              }}
            >
              Communities
            </div>

            <div
              style={{
                fontSize: "42px",
                fontWeight: "700",
              }}
            >
              {clusters.length}
            </div>
          </div>

          <div
            style={{
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "18px",
              padding: "25px",
            }}
          >
            <div
              style={{
                color: "#38bdf8",
                fontSize: "15px",
                marginBottom: "10px",
              }}
            >
              Components
            </div>

            <div
              style={{
                fontSize: "42px",
                fontWeight: "700",
              }}
            >
              {totalComponents}
            </div>
          </div>
        </div>
      )}

      {/* Loading */}

      {loading && (
        <div
          style={{
            background: "#1e293b",
            border: "1px solid #334155",
            borderRadius: "18px",
            padding: "40px",
            textAlign: "center",
            color: "#94a3b8",
          }}
        >
          Loading architecture communities...
        </div>
      )}

      {/* Error */}

      {error && (
        <div
          style={{
            background: "#7f1d1d",
            border: "1px solid #ef4444",
            borderRadius: "18px",
            padding: "25px",
            color: "#fecaca",
          }}
        >
          Error: {error}
        </div>
      )}

      {/* Communities */}

      {!loading &&
        !error &&
        clusters.map((cluster) => (
          <div
            key={cluster.cluster_id}
            style={{
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "18px",
              padding: "24px",
              marginBottom: "20px",
              transition: "all 0.25s ease",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "15px",
                flexWrap: "wrap",
                gap: "15px",
              }}
            >
              <div>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                  }}
                >
                  <FaLayerGroup
                    color="#38bdf8"
                    size={20}
                  />

                  <h2
                    style={{
                      margin: 0,
                      fontSize: "28px",
                      color: "#38bdf8",
                    }}
                  >
                    {cluster.cluster_name}
                  </h2>
                </div>

                <div
                  style={{
                    color: "#94a3b8",
                    marginTop: "8px",
                  }}
                >
                  Software architecture module
                </div>
              </div>

              <div
                style={{
                  background: "#0f172a",
                  border: "1px solid #334155",
                  borderRadius: "14px",
                  padding: "14px 18px",
                  textAlign: "center",
                  minWidth: "120px",
                }}
              >
                <div
                  style={{
                    color: "#38bdf8",
                    fontSize: "13px",
                  }}
                >
                  Components
                </div>

                <div
                  style={{
                    fontSize: "30px",
                    fontWeight: "700",
                  }}
                >
                  {cluster.size}
                </div>
              </div>
            </div>

            <details>
              <summary
                style={{
                  cursor: "pointer",
                  color: "#f59e0b",
                  fontWeight: "600",
                  fontSize: "15px",
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  listStyle: "none",
                }}
              >
                <FaChevronDown />
                View Components
              </summary>

              <div
                style={{
                  marginTop: "20px",
                  maxHeight: "350px",
                  overflowY: "auto",
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(250px, 1fr))",
                  gap: "12px",
                }}
              >
                {(cluster.members || []).map((member) => (
                  <div
                    key={member}
                    style={{
                      background: "#0f172a",
                      border: "1px solid #334155",
                      borderRadius: "12px",
                      padding: "14px",
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      transition: "all 0.2s ease",
                    }}
                  >
                    <FaProjectDiagram
                      color="#38bdf8"
                      size={14}
                    />

                    <span
                      style={{
                        color: "#e2e8f0",
                        fontSize: "14px",
                        wordBreak: "break-word",
                      }}
                    >
                      {member}
                    </span>
                  </div>
                ))}
              </div>
            </details>
          </div>
        ))}

      {/* Empty State */}

      {!loading &&
        !error &&
        clusters.length === 0 && (
          <div
            style={{
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "18px",
              padding: "40px",
              textAlign: "center",
            }}
          >
            <FaUsers
              size={40}
              color="#64748b"
            />

            <h3
              style={{
                marginTop: "20px",
              }}
            >
              No Communities Found
            </h3>

            <p
              style={{
                color: "#94a3b8",
              }}
            >
              Analyze a repository first to generate architecture
              communities.
            </p>
          </div>
        )}
    </div>
  );
}