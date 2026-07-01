import ClusterGraph from "../components/ClusterGraph";
import ArchitectureExplorer from "../components/ArchitectureExplorer";
import ArchitectureClusters from "../components/ArchitectureClusters";
import ArchitectureLayers from "../components/ArchitectureLayers";

export default function ArchitecturePage({
    selectedCluster,
    setSelectedCluster,
    selectedComponent,
    setSelectedComponent
}) {

    return (

        <div>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "60% 40%",
                    gap: "20px"
                }}
            >

                <div
                    style={{
                        height: "700px",
                        border:
                            "1px solid #1e293b",
                        borderRadius: "12px"
                    }}
                >
                    <ClusterGraph
                        onClusterSelect={
                            setSelectedCluster
                        }
                    />
                </div>

                <ArchitectureExplorer
                    selectedComponent={
                        selectedComponent
                    }
                    selectedCluster={
                        selectedCluster
                    }
                />

            </div>

            <br />

            <ArchitectureClusters />

            <br />

            <ArchitectureLayers />

        </div>
    );
} 