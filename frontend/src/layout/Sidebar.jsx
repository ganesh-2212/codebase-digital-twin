import {
    FaChartPie,
    FaDatabase,
    FaProjectDiagram,
    FaLayerGroup,
    FaHeartbeat,
    FaExclamationTriangle,
    FaExchangeAlt,
    FaBolt,
    FaShieldAlt,
    FaRobot,
    FaCircle
} from "react-icons/fa";

import { HiUsers } from "react-icons/hi";

export default function Sidebar({
    activeSection,
    setActiveSection
}) {

    const sections = [
        {
            title: "Overview",
            items: [
                {
                    key: "dashboard",
                    label: "Dashboard",
                    icon: <FaChartPie size={15} />
                },
                {
                    key: "analyze",
                    label: "Repository",
                    icon: <FaDatabase size={15} />
                }
            ]
        },

        {
            title: "Architecture",
            items: [
                {
                    key: "architecture",
                    label: "Architecture Graph",
                    icon: <FaProjectDiagram size={15} />
                },
                {
                    key: "communities",
                    label: "Communities",
                    icon: <HiUsers size={15} />
                },
                {
                    key: "layers",
                    label: "Layers",
                    icon: <FaLayerGroup size={15} />
                },
                {
                    key: "violations",
                    label: "Layer Violations",
                    icon: <FaExclamationTriangle size={15} />
                },
                {
                    key: "health",
                    label: "Architecture Health",
                    icon: <FaHeartbeat size={15} />
                }
            ]
        },

        {
            title: "AI Intelligence",
            items: [
                {
                    key: "impact",
                    label: "Impact Analysis",
                    icon: <FaBolt size={15} />
                },
                {
                    key: "prediction",
                    label: "Change Prediction",
                    icon: <FaExchangeAlt size={15} />
                },
                {
                    key: "quality",
                    label: "Quality",
                    icon: <FaShieldAlt size={15} />
                },
                {
                    key: "chat",
                    label: "AI Chat",
                    icon: <FaRobot size={15} />
                }
            ]
        }
    ];

    return (
        <div
            style={{
                width: "270px",
                background: "#0b1220",
                borderRight: "1px solid #1e293b",
                padding: "20px 14px",
                minHeight: "100vh",
                overflowY: "auto",
                flexShrink: 0
            }}
        >
            {/* Header */}

            <div
                style={{
                    marginBottom: "28px",
                    paddingBottom: "22px",
                    borderBottom: "1px solid #1e293b"
                }}
            >
                <div
                    style={{
                        fontSize: "22px",
                        fontWeight: "700",
                        color: "#f8fafc",
                        marginBottom: "6px"
                    }}
                >
                    Codebase Twin
                </div>

                <div
                    style={{
                        color: "#64748b",
                        fontSize: "12px",
                        lineHeight: "1.6"
                    }}
                >
                    AI-powered repository intelligence platform
                </div>

                <div
                    style={{
                        marginTop: "16px",
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        fontSize: "12px",
                        color: "#4ade80"
                    }}
                >
                    <FaCircle
                        size={8}
                        color="#22c55e"
                    />
                    Backend Connected
                </div>
            </div>

            {sections.map(group => (
                <div
                    key={group.title}
                    style={{
                        marginBottom: "22px"
                    }}
                >
                    <div
                        style={{
                            color: "#64748b",
                            fontSize: "11px",
                            fontWeight: "700",
                            textTransform: "uppercase",
                            letterSpacing: "1px",
                            marginBottom: "10px",
                            paddingLeft: "10px"
                        }}
                    >
                        {group.title}
                    </div>

                    {group.items.map(section => {

                        const active =
                            activeSection === section.key;

                        return (
                            <div
                                key={section.key}
                                onClick={() =>
                                    setActiveSection(
                                        section.key
                                    )
                                }
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "14px",

                                    padding:
                                        "12px 14px",

                                    marginBottom:
                                        "4px",

                                    borderRadius:
                                        "12px",

                                    cursor:
                                        "pointer",

                                    transition:
                                        "all 0.2s ease",

                                    background:
                                        active
                                            ? "linear-gradient(90deg,#1d4ed8,#2563eb)"
                                            : "transparent",

                                    color:
                                        active
                                            ? "#ffffff"
                                            : "#94a3b8",

                                    fontWeight:
                                        active
                                            ? "600"
                                            : "500",

                                    boxShadow:
                                        active
                                            ? "0 0 20px rgba(37,99,235,0.25)"
                                            : "none"
                                }}
                            >
                                <div
                                    style={{
                                        color:
                                            active
                                                ? "#ffffff"
                                                : "#64748b"
                                    }}
                                >
                                    {section.icon}
                                </div>

                                <span
                                    style={{
                                        fontSize: "14px"
                                    }}
                                >
                                    {section.label}
                                </span>
                            </div>
                        );
                    })}
                </div>
            ))}

            
        </div>
    );
}