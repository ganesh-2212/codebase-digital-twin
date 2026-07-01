import RepositoryChat from "./RepositoryChat";
import { FaRobot } from "react-icons/fa";

export default function AssistantPage() {
    return (
        <div
            style={{
                width: "100%",
                padding: "10px 0"
            }}
        >
            {/* Header */}

            <div
                style={{
                    marginBottom: "24px"
                }}
            >
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                        marginBottom: "10px"
                    }}
                >
                    <div
                        style={{
                            width: "50px",
                            height: "50px",
                            borderRadius: "14px",
                            background:
                                "linear-gradient(135deg,#2563eb,#3b82f6)",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            fontSize: "20px",
                            color: "white"
                        }}
                    >
                        <FaRobot />
                    </div>

                    <div>
                        <h1
                            style={{
                                margin: 0,
                                fontSize: "30px",
                                fontWeight: "700",
                                color: "#f8fafc"
                            }}
                        >
                            AI Architecture Assistant
                        </h1>

                        <div
                            style={{
                                color: "#94a3b8",
                                marginTop: "6px",
                                fontSize: "15px"
                            }}
                        >
                            Ask questions about repository structure,
                            dependencies, architecture decisions,
                            impact analysis and code relationships.
                        </div>
                    </div>
                </div>
            </div>

            {/* Chat Container */}

            <div
                style={{
                    background: "#111827",
                    border: "1px solid #1e293b",
                    borderRadius: "18px",
                    overflow: "hidden",
                    boxShadow:
                        "0 10px 30px rgba(0,0,0,0.25)"
                }}
            >
                <RepositoryChat />
            </div>
        </div>
    );
}