import React, { useEffect, useState } from "react";
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
} from "reactflow";

import dagre from "dagre";

import "reactflow/dist/style.css";

/* ==========================================
   DAGRE AUTO LAYOUT
========================================== */

const nodeWidth = 180;
const nodeHeight = 60;

function getLayoutedElements(nodes, edges) {
  const dagreGraph = new dagre.graphlib.Graph();

  dagreGraph.setDefaultEdgeLabel(() => ({}));

  dagreGraph.setGraph({
    rankdir: "LR",
    ranksep: 120,
    nodesep: 80,
  });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, {
      width: nodeWidth,
      height: nodeHeight,
    });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(
      edge.source,
      edge.target
    );
  });

  dagre.layout(dagreGraph);

  return nodes.map((node) => {
    const position = dagreGraph.node(node.id);

    return {
      ...node,
      position: {
        x: position.x - nodeWidth / 2,
        y: position.y - nodeHeight / 2,
      },
    };
  });
}

export default function ArchitectureGraph({
  onNodeSelect,
}) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    async function loadGraph() {
      try {
        const graphResponse = await fetch(
          "http://127.0.0.1:8000/architecture-graph"
        );

        const heatmapResponse = await fetch(
          "http://127.0.0.1:8000/architecture_heatmap"
        );

        const graphData =
          await graphResponse.json();

        const heatmapData =
          await heatmapResponse.json();

        console.log(
          "Nodes:",
          graphData.nodes?.length
        );

        console.log(
          "Edges:",
          graphData.edges?.length
        );

        const heatmap = {};

        heatmapData.forEach((item) => {
          heatmap[item.name] =
            item.impact_level;
        });

        const flowNodes =
          graphData.nodes.map((node) => {
            let borderColor =
              "#38bdf8";

            const level =
              heatmap[node.label];

            if (level === "HIGH") {
              borderColor =
                "#ef4444";
            } else if (
              level === "MEDIUM"
            ) {
              borderColor =
                "#f59e0b";
            } else if (
              level === "LOW"
            ) {
              borderColor =
                "#22c55e";
            }

            return {
              id: String(node.id),

              data: {
                label: node.label,
              },

              position: {
                x: 0,
                y: 0,
              },

              style: {
                background:
                  "#1e293b",

                color: "#ffffff",

                border: `3px solid ${borderColor}`,

                borderRadius:
                  "12px",

                padding: "10px",

                width: 180,

                textAlign:
                  "center",

                fontSize:
                  "12px",

                fontWeight:
                  "bold",
              },
            };
          });

        const flowEdges =
          graphData.edges.map(
            (edge, index) => ({
              id: `e${index}`,

              source: String(
                edge.source
              ),

              target: String(
                edge.target
              ),

              animated: true,

              style: {
                stroke:
                  "#64748b",

                strokeWidth: 2,
              },
            })
          );

        const layoutedNodes =
          getLayoutedElements(
            flowNodes,
            flowEdges
          );

        console.log(
          "Layouted Nodes:",
          layoutedNodes
        );

        setNodes(layoutedNodes);
        setEdges(flowEdges);
      } catch (error) {
        console.error(
          "Graph Load Error:",
          error
        );
      }
    }

    loadGraph();
  }, []);

  /* ==========================================
     NODE CLICK
  ========================================== */

  const handleNodeClick = (
    _,
    node
  ) => {
    if (onNodeSelect) {
      onNodeSelect(
        node.data.label
      );
    }

    setNodes((prev) =>
      prev.map((n) => ({
        ...n,

        style: {
          ...n.style,

          boxShadow:
            n.id === node.id
              ? "0 0 20px #f59e0b"
              : "none",
        },
      }))
    );
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        minHeight: "900px",
        border: "1px solid #333",
        borderRadius: "12px",
        overflow: "hidden",
        background: "#0f172a",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{
          padding: 1.0,
        }}
        minZoom={0.05}
        maxZoom={2}
        panOnDrag
        zoomOnScroll
        zoomOnPinch
        nodesDraggable
        onNodeClick={
          handleNodeClick
        }
      >
        <MiniMap
          pannable
          zoomable
          nodeColor={(node) => {
            const border =
              node.style?.border ||
              "";

            if (
              border.includes(
                "#ef4444"
              )
            ) {
              return "#ef4444";
            }

            if (
              border.includes(
                "#f59e0b"
              )
            ) {
              return "#f59e0b";
            }

            if (
              border.includes(
                "#22c55e"
              )
            ) {
              return "#22c55e";
            }

            return "#38bdf8";
          }}
        />

        <Controls />

        <Background
          gap={20}
          size={1}
          color="#334155"
        />
      </ReactFlow>
    </div>
  );
}