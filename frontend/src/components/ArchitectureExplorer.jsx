import { useState, useEffect } from "react";

export default function ArchitectureExplorer({
    selectedComponent,
    selectedCluster,
}) {
    const [clusterComponents, setClusterComponents] = useState([]);
    const [component, setComponent] = useState(null);
    const [loading, setLoading] = useState(false);
    const [activeComponent, setActiveComponent] = useState(null);

    useEffect(() => {
        if (!selectedCluster) return;

        setComponent(null);
        setActiveComponent(null);

        setLoading(true);

        fetch(
            `http://localhost:8000/cluster-details/${selectedCluster}`
        )
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    setClusterComponents(
                        data.components || []
                    );
                }
            })
            .finally(() => setLoading(false));
    }, [selectedCluster]);

    useEffect(() => {
        const componentName =
            activeComponent ||
            selectedComponent;

        if (!componentName) return;

        setLoading(true);

        fetch(
            `http://localhost:8000/component/${componentName}`
        )
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    setComponent(data);
                }
            })
            .finally(() => setLoading(false));
    }, [
        activeComponent,
        selectedComponent,
    ]);

    function openComponent(name) {
        setActiveComponent(name);
    }

    const panelStyle = {
        background: "#111827",
        border: "1px solid #1e293b",
        borderRadius: "16px",
        padding: "24px",
        height: "700px",
        overflowY: "auto",
    };

    const chipStyle = {
        background: "#1e293b",
        border: "1px solid #334155",
        borderRadius: "10px",
        padding: "10px 14px",
        color: "#e2e8f0",
        marginBottom: "10px",
        fontSize: "14px",
    };

    if (!selectedCluster) {
        return (
            <div style={panelStyle}>
                <div
                    style={{
                        display: "flex",
                        height: "100%",
                        justifyContent: "center",
                        alignItems: "center",
                        color: "#64748b",
                        textAlign: "center",
                    }}
                >
                    <div>
                        <h2
                            style={{
                                color: "#38bdf8",
                                marginBottom: "10px",
                            }}
                        >
                            Architecture Explorer
                        </h2>

                        <p>
                            Select a cluster from the graph
                            to inspect components.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    if (
        selectedCluster &&
        !component
    ) {
        return (
            <div style={panelStyle}>
                <div
                    style={{
                        marginBottom: "25px",
                    }}
                >
                    <div
                        style={{
                            color: "#38bdf8",
                            fontSize: "14px",
                            marginBottom: "6px",
                        }}
                    >
                        Cluster
                    </div>

                    <h2
                        style={{
                            margin: 0,
                            fontSize: "28px",
                        }}
                    >
                        {selectedCluster}
                    </h2>

                    <p
                        style={{
                            color: "#94a3b8",
                            marginTop: "10px",
                        }}
                    >
                        {clusterComponents.length} components
                        discovered
                    </p>
                </div>

                {loading ? (
                    <div
                        style={{
                            color: "#94a3b8",
                        }}
                    >
                        Loading cluster...
                    </div>
                ) : (
                    clusterComponents.map((item) => (
                        <div
                            key={item}
                            onClick={() =>
                                openComponent(item)
                            }
                            style={{
                                ...chipStyle,
                                cursor: "pointer",
                                transition: "0.2s",
                            }}
                        >
                            {item}
                        </div>
                    ))
                )}
            </div>
        );
    }

    return (
        <div style={panelStyle}>
            {loading && (
                <div
                    style={{
                        color: "#94a3b8",
                    }}
                >
                    Loading component...
                </div>
            )}

            {!loading &&
                component &&
                component.success && (
                    <>
                        <button
                            onClick={() => {
                                setComponent(null);
                                setActiveComponent(
                                    null
                                );
                            }}
                            style={{
                                background: "#1e293b",
                                border: "1px solid #334155",
                                color: "#cbd5e1",
                                borderRadius: "10px",
                                padding: "10px 16px",
                                cursor: "pointer",
                                marginBottom: "25px",
                            }}
                        >
                            ← Back to Cluster
                        </button>

                        <h1
                            style={{
                                marginBottom: "12px",
                                fontSize: "34px",
                            }}
                        >
                            {component.name}
                        </h1>

                        <div
                            style={{
                                display: "flex",
                                flexWrap: "wrap",
                                gap: "10px",
                                marginBottom: "25px",
                            }}
                        >
                            <div style={chipStyle}>
                                Type: {component.type}
                            </div>

                            <div style={chipStyle}>
                                Cluster: {component.cluster}
                            </div>

                            <div style={chipStyle}>
                                Impact Score:{" "}
                                {component.impact_score}
                            </div>
                        </div>

                        <div
                            style={{
                                background: "#0f172a",
                                border:
                                    "1px solid #1e293b",
                                padding: "14px",
                                borderRadius: "12px",
                                marginBottom: "25px",
                            }}
                        >
                            <div
                                style={{
                                    color: "#64748b",
                                    fontSize: "13px",
                                    marginBottom: "6px",
                                }}
                            >
                                SOURCE FILE
                            </div>

                            <div
                                style={{
                                    color: "#38bdf8",
                                    wordBreak:
                                        "break-all",
                                }}
                            >
                                {component.file}
                            </div>
                        </div>

                        <h3
                            style={{
                                marginBottom: "15px",
                            }}
                        >
                            Dependencies
                        </h3>

                        {(component.calls || [])
                            .length === 0 ? (
                            <div
                                style={{
                                    color: "#64748b",
                                    marginBottom: "25px",
                                }}
                            >
                                No dependencies
                            </div>
                        ) : (
                            component.calls.map(
                                (call) => (
                                    <div
                                        key={call}
                                        style={
                                            chipStyle
                                        }
                                    >
                                        {call}
                                    </div>
                                )
                            )
                        )}

                        <h3
                            style={{
                                marginTop: "30px",
                                marginBottom:
                                    "15px",
                            }}
                        >
                            Dependents
                        </h3>

                        {(component.called_by || [])
                            .length === 0 ? (
                            <div
                                style={{
                                    color: "#64748b",
                                }}
                            >
                                No dependents
                            </div>
                        ) : (
                            component.called_by.map(
                                (call) => (
                                    <div
                                        key={call}
                                        style={
                                            chipStyle
                                        }
                                    >
                                        {call}
                                    </div>
                                )
                            )
                        )}
                    </>
                )}
        </div>
    );
}