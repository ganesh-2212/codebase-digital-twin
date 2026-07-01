import { useEffect, useState } from "react";

import ReactFlow, {
  Controls,
  MiniMap,
  Background,
  MarkerType,
} from "reactflow";

import "reactflow/dist/style.css";

export default function ClusterGraph({ onClusterSelect }) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/cluster-graph")
      .then((res) => res.json())
      .then((data) => {

        const rfNodes = data.nodes.map((node, index) => {
          const column = index % 5;
          const row = Math.floor(index / 5);

          const size =
            node.size > 50
              ? 220
              : node.size > 25
              ? 190
              : 170;

          return {
            id: String(node.id),

            data: {
              label: (
                <div
                  style={{
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontWeight: 700,
                      fontSize: "14px",
                      marginBottom: "8px",
                    }}
                  >
                    {node.label}
                  </div>

                  <div
                    style={{
                      fontSize: "12px",
                      color: "#94a3b8",
                    }}
                  >
                    {node.size} Components
                  </div>
                </div>
              ),
            },

            position: {
              x: column * 260,
              y: row * 180,
            },

            style: {
              width: size,
              height: 95,

              borderRadius: "18px",

              background:
                "linear-gradient(145deg,#111827,#1e293b)",

              border: "1px solid #334155",

              color: "#ffffff",

              display: "flex",
              alignItems: "center",
              justifyContent: "center",

              boxShadow:
                "0 10px 25px rgba(0,0,0,0.35)",

              transition: "all 0.3s ease",
            },
          };
        });

        const rfEdges = (data.edges || []).map(
          (edge, index) => ({
            id: `edge-${index}`,

            source: String(edge.source),

            target: String(edge.target),

            animated: true,

            markerEnd: {
              type: MarkerType.ArrowClosed,
              color: "#475569",
            },

            style: {
              stroke: "#475569",
              strokeWidth: 2,
            },
          })
        );

        setNodes(rfNodes);
        setEdges(rfEdges);
      });
  }, []);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#0f172a",
        borderRadius: "18px",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{
          padding: 0.25,
        }}
        minZoom={0.2}
        maxZoom={2.5}
        onNodeClick={(_, node) => {
          onClusterSelect?.(node.id);
        }}
      >
        <MiniMap
          zoomable
          pannable
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "12px",
          }}
        />

        <Controls
          style={{
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "12px",
          }}
        />

        <Background
          color="#1e293b"
          gap={28}
          size={1}
        />
      </ReactFlow>
    </div>
  );
}