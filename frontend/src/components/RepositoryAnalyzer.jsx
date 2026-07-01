import { useState } from "react";
import {
  FaGithub,
  FaSpinner,
  FaCheckCircle,
  FaProjectDiagram,
  FaCodeBranch,
  FaCube,
  FaUsers
} from "react-icons/fa";

export default function RepositoryAnalyzer({
  setAnalysisComplete,
  setRepository,
}) {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [repoInfo, setRepoInfo] = useState(null);

  async function analyze() {
    if (!repoUrl.trim()) {
      alert("Please enter a GitHub repository URL");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze-repository",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repo_url: repoUrl.trim(),
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setRepository(repoUrl.trim());
        setAnalysisComplete(true);

        setRepoInfo({
          repo: repoUrl.trim(),
          nodes:
            data.dependency_nodes ??
            data.nodes ??
            0,

          edges:
            data.dependency_edges ??
            data.edges ??
            0,

          components:
            data.architecture_summaries ??
            data.components ??
            0,

          communities:
            data.clusters ?? 0,
        });
      } else {
        alert(
          data.error ||
            "Repository analysis failed."
        );
      }
    } catch (err) {
      console.error(err);

      alert(
        "Cannot connect to backend server."
      );
    }

    setLoading(false);
  }

  const metricCard = (
    title,
    value,
    icon,
    color
  ) => (
    <div
      style={{
        background: "#1e293b",
        border: "1px solid #334155",
        borderRadius: "14px",
        padding: "20px",
        minWidth: "180px",
        flex: 1,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center",
          marginBottom: "15px",
          color: "#94a3b8",
          fontSize: "14px",
        }}
      >
        {title}
        <span
          style={{
            color,
            fontSize: "20px",
          }}
        >
          {icon}
        </span>
      </div>

      <div
        style={{
          fontSize: "32px",
          fontWeight: "700",
          color,
        }}
      >
        {value}
      </div>
    </div>
  );

  return (
    <div
      style={{
        background: "#111827",
        border:
          "1px solid #1e293b",
        borderRadius: "20px",
        padding: "35px",
      }}
    >
      {/* Header */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          marginBottom: "25px",
        }}
      >
        <FaGithub
          size={28}
          color="#38bdf8"
        />

        <div>
          <h2
            style={{
              margin: 0,
              fontSize: "28px",
            }}
          >
            Repository Analysis
          </h2>

          <div
            style={{
              color: "#94a3b8",
              marginTop: "5px",
            }}
          >
            Analyze software architecture using GraphRAG intelligence
          </div>
        </div>
      </div>

      {/* Input */}

      <div
        style={{
          display: "flex",
          gap: "15px",
          marginBottom: "30px",
        }}
      >
        <input
          type="text"
          value={repoUrl}
          onChange={(e) =>
            setRepoUrl(
              e.target.value
            )
          }
          placeholder="https://github.com/user/repository"
          style={{
            flex: 1,
            padding: "18px",
            borderRadius: "14px",
            border:
              "1px solid #334155",
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
              "18px 30px",
            borderRadius:
              "14px",
            border: "none",
            background:
              "#2563eb",
            color: "white",
            fontWeight: "600",
            cursor: "pointer",
            minWidth: "220px",
          }}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Repository"}
        </button>
      </div>

      {/* Loading */}

      {loading && (
        <div
          style={{
            background:
              "#1e293b",
            border:
              "1px solid #334155",
            borderRadius:
              "14px",
            padding: "25px",
            lineHeight: "2.3",
            color: "#cbd5e1",
          }}
        >
          {[
            "Cloning Repository",
            "Parsing Source Files",
            "Building Dependency Graph",
            "Detecting Communities",
            "Generating GraphRAG Context",
            "Computing Architecture Intelligence",
          ].map(
            (
              step
            ) => (
              <div
                key={
                  step
                }
              >
                <FaSpinner
                  style={{
                    marginRight:
                      "12px",
                  }}
                />
                {step}
              </div>
            )
          )}
        </div>
      )}

      {/* Repository Results */}

      {repoInfo && (
        <>
          {/* Hero Card */}

          <div
            style={{
              marginTop: "30px",
              background:
                "#1e293b",
              border:
                "1px solid #334155",
              borderRadius:
                "18px",
              padding: "30px",
            }}
          >
            <div
              style={{
                display:
                  "flex",
                justifyContent:
                  "space-between",
                alignItems:
                  "center",
                flexWrap:
                  "wrap",
                gap: "20px",
              }}
            >
              <div>
                <div
                  style={{
                    color:
                      "#38bdf8",
                    fontSize:
                      "14px",
                    marginBottom:
                      "10px",
                  }}
                >
                  Repository Intelligence
                </div>

                <h1
                  style={{
                    margin:
                      "0 0 10px 0",
                    fontSize:
                      "32px",
                  }}
                >
                  {
                    repoInfo.repo
                  }
                </h1>

                <div
                  style={{
                    color:
                      "#94a3b8",
                  }}
                >
                  GraphRAG-powered architecture analysis completed
                </div>
              </div>

              <div
                style={{
                  background:
                    "#14532d",
                  color:
                    "#4ade80",
                  padding:
                    "10px 18px",
                  borderRadius:
                    "999px",
                  fontWeight:
                    "600",
                }}
              >
                <FaCheckCircle
                  style={{
                    marginRight:
                      "8px",
                  }}
                />
                Analysis Complete
              </div>
            </div>

            {/* Tech badges */}

            <div
              style={{
                display:
                  "flex",
                gap: "10px",
                flexWrap:
                  "wrap",
                marginTop:
                  "25px",
              }}
            >
              {[
                "FastAPI",
                "GraphRAG",
                "ChromaDB",
                "NetworkX",
                "React",
              ].map(
                (
                  tech
                ) => (
                  <div
                    key={
                      tech
                    }
                    style={{
                      padding:
                        "8px 14px",
                      borderRadius:
                        "999px",
                      background:
                        "#0f172a",
                      border:
                        "1px solid #334155",
                      color:
                        "#38bdf8",
                      fontSize:
                        "13px",
                    }}
                  >
                    {tech}
                  </div>
                )
              )}
            </div>
          </div>

          {/* Metrics */}

          <div
            style={{
              display: "flex",
              gap: "20px",
              flexWrap:
                "wrap",
              marginTop: "25px",
            }}
          >
            {metricCard(
              "Dependency Nodes",
              repoInfo.nodes,
              <FaProjectDiagram />,
              "#38bdf8"
            )}

            {metricCard(
              "Dependency Edges",
              repoInfo.edges,
              <FaCodeBranch />,
              "#22c55e"
            )}

            {metricCard(
              "Components",
              repoInfo.components,
              <FaCube />,
              "#a855f7"
            )}

            {metricCard(
              "Communities",
              repoInfo.communities,
              <FaUsers />,
              "#f59e0b"
            )}
          </div>

          {/* Pipeline */}

          <div
            style={{
              marginTop: "25px",
              background:
                "#1e293b",
              border:
                "1px solid #334155",
              borderRadius:
                "14px",
              padding: "25px",
            }}
          >
            <h3
              style={{
                color:
                  "#38bdf8",
                marginBottom:
                  "20px",
              }}
            >
              Analysis Pipeline
            </h3>

            <div
              style={{
                display:
                  "flex",
                gap: "12px",
                flexWrap:
                  "wrap",
              }}
            >
              {[
                "AST Parsing",
                "Dependency Graph",
                "Community Detection",
                "GraphRAG",
                "Architecture Intelligence",
              ].map(
                (
                  stage
                ) => (
                  <div
                    key={
                      stage
                    }
                    style={{
                      background:
                        "#0f172a",
                      border:
                        "1px solid #334155",
                      borderRadius:
                        "999px",
                      padding:
                        "10px 18px",
                      color:
                        "#cbd5e1",
                    }}
                  >
                    {stage}
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