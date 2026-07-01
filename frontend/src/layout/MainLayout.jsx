import { useState } from "react";

import Dashboard from "../pages/Dashboard";
import RepositoryChat from "../pages/RepositoryChat";
import ImpactAnalysis from "../pages/ImpactAnalysis";

import RepositoryAnalyzer from "../components/RepositoryAnalyzer";
import RepositoryStats from "../components/RepositoryStats";

import ClusterGraph from "../components/ClusterGraph";
import ArchitectureExplorer from "../components/ArchitectureExplorer";
import ArchitectureClusters from "../components/ArchitectureClusters";
import ArchitectureLayers from "../components/ArchitectureLayers";

import ImpactHeatmap from "../components/ImpactHeatmap";
import SmellDetection from "../components/SmellDetection";
import ArchitectureHealth from "../components/ArchitectureHealth";
import ChangePrediction from "../components/ChangePrediction";
import LayerViolations from "../components/LayerViolations";

import Sidebar from "./Sidebar";

export default function MainLayout() {
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [selectedCluster, setSelectedCluster] = useState(null);

  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [, setRepository] = useState("");
  const [activeSection, setActiveSection] = useState("dashboard");

  const renderIfReady = (component) => {
    if (
      !analysisComplete &&
      activeSection !== "dashboard" &&
      activeSection !== "analyze"
    ) {
      return (
        <div
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "500px",
          }}
        >
          <div
            style={{
              background: "#111827",
              border: "1px solid #334155",
              borderRadius: "20px",
              padding: "50px",
              textAlign: "center",
              maxWidth: "550px",
            }}
          >
            <h2
              style={{
                color: "#38bdf8",
                marginBottom: "15px",
                fontSize: "30px",
              }}
            >
              Repository Required
            </h2>

            <p
              style={{
                color: "#94a3b8",
                fontSize: "16px",
                lineHeight: "1.8",
              }}
            >
              Analyze a repository first to unlock architecture intelligence,
              GraphRAG retrieval, impact analysis, and AI insights.
            </p>
          </div>
        </div>
      );
    }

    return component;
  };

  return (
    <div
      style={{
        display: "flex",
        width: "100vw",
        height: "100vh",
        background: "#0b1120",
        color: "white",
        overflow: "hidden",
      }}
    >
      <Sidebar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
      />

      <div
        style={{
          flex: 1,
          minWidth: 0,
          height: "100%",
          padding: "30px",
          overflowY: "auto",
          overflowX: "hidden",
          boxSizing: "border-box",
        }}
      >
        {activeSection === "dashboard" && <Dashboard />}

        {activeSection === "analyze" && (
          <>
            <RepositoryAnalyzer
              setAnalysisComplete={setAnalysisComplete}
              setRepository={setRepository}
            />

            {analysisComplete && (
              <div
                style={{
                  marginTop: "30px",
                }}
              >
                <RepositoryStats />
              </div>
            )}
          </>
        )}

        {activeSection === "architecture" &&
          renderIfReady(
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "2fr 1fr",
                gap: "20px",
                width: "100%",
              }}
            >
              <div
                style={{
                  height: "720px",
                  border: "1px solid #1e293b",
                  borderRadius: "18px",
                  overflow: "hidden",
                  background: "#111827",
                }}
              >
                <ClusterGraph
                  onClusterSelect={setSelectedCluster}
                />
              </div>

              <ArchitectureExplorer
                selectedComponent={selectedComponent}
                selectedCluster={selectedCluster}
              />
            </div>
          )}

        {activeSection === "communities" &&
          renderIfReady(<ArchitectureClusters />)}

        {activeSection === "layers" &&
          renderIfReady(<ArchitectureLayers />)}

        {activeSection === "violations" &&
          renderIfReady(<LayerViolations />)}

        {activeSection === "health" &&
          renderIfReady(<ArchitectureHealth />)}

        {activeSection === "impact" &&
          renderIfReady(
            <>
              <ImpactAnalysis />

              <div
                style={{
                  height: "30px",
                }}
              />

              <ImpactHeatmap />
            </>
          )}

        {activeSection === "quality" &&
          renderIfReady(
            <>
              <ArchitectureHealth />

              <div
                style={{
                  height: "30px",
                }}
              />

              <SmellDetection />
            </>
          )}

        {activeSection === "prediction" &&
          renderIfReady(<ChangePrediction />)}

        {activeSection === "chat" &&
          renderIfReady(<RepositoryChat />)}

        <div
          style={{
            marginTop: "80px",
            paddingTop: "35px",
            borderTop: "1px solid #1e293b",
            textAlign: "center",
            color: "#64748b",
            fontSize: "13px",
            lineHeight: "1.8",
            opacity: 0.75,
          }}
        >
          <div
            style={{
              color: "#38bdf8",
              fontWeight: "700",
              fontSize: "18px",
              marginBottom: "6px",
            }}
          >
            Codebase Digital Twin
          </div>

          <div>
            AI-Powered Software Architecture Intelligence Platform
          </div>
        </div>
      </div>
    </div>
  );
}