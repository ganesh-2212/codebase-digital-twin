import { useEffect, useState } from "react";

import ReactFlow, {
  Controls,
  MiniMap,
  Background,
  MarkerType,
} from "reactflow";

import "reactflow/dist/style.css";

export default function ArchitectureGraph({
  onNodeSelect,
}) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    fetch(
      "http://localhost:8000/architecture-graph"
    )
      .then((res) => res.json())
      .then((data) => {
        console.log(
          "Backend Nodes:",
          data.nodes.length
        );

        console.log(
          "Backend Edges:",
          data.edges.length
        );

        const limitedNodes =
          data.nodes.slice(0, 300);

        const allowedIds = new Set(
          limitedNodes.map((n) =>
            String(n.id)
          )
        );

        const limitedEdges =
          data.edges.filter(
            (edge) =>
              allowedIds.has(
                String(edge.source)
              ) &&
              allowedIds.has(
                String(edge.target)
              )
          );

        const rfNodes =
          limitedNodes.map(
            (node, index) => {
              const column =
                index % 10;

              const row =
                Math.floor(
                  index / 10
                );

              return {
                id: String(node.id),

                data: {
                  label:
                    node.label,
                  full_name:
                    node.full_name ||
                    node.label,
                },

                position: {
                  x:
                    column *
                    250,
                  y:
                    row * 120,
                },

                style: {
                  width: 180,
                  padding: 10,
                  borderRadius:
                    10,
                  border:
                    "1px solid #475569",

                  background:
                    node.type ===
                    "class"
                      ? "#1e293b"
                      : "#0f172a",

                  color:
                    "white",

                  fontSize: 12,

                  textAlign:
                    "center",
                },
              };
            }
          );

        const rfEdges =
          limitedEdges.map(
            (
              edge,
              index
            ) => ({
              id:
                `edge-${index}`,

              source:
                String(
                  edge.source
                ),

              target:
                String(
                  edge.target
                ),

              animated:
                false,

              markerEnd:
                {
                  type:
                    MarkerType.ArrowClosed,
                },

              style: {
                stroke:
                  "#64748b",
              },
            })
          );

        setNodes(
          rfNodes
        );

        setEdges(
          rfEdges
        );
      })

      .catch((err) => {
        console.error(
          "Architecture Graph Error:",
          err
        );
      });
  }, []);

  return (
    <div
      style={{
        width: "100%",
        height: "1000px",
        border:
          "1px solid #444",
        borderRadius:
          "10px",
        overflow:
          "hidden",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        minZoom={0.05}
        maxZoom={2}
        onNodeClick={(
          event,
          node
        ) => {
          if (
            onNodeSelect
          ) {
            onNodeSelect(
              node.data
                .full_name
            );
          }
        }}
      >
        <MiniMap
          zoomable
          pannable
        />

        <Controls />

        <Background
          gap={20}
          size={1}
        />
      </ReactFlow>
    </div>
  );
}