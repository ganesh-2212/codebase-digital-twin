import { useState } from "react";
import {
    FaRobot,
    FaPaperPlane,
    FaSpinner,
    FaBrain
} from "react-icons/fa";

export default function RepositoryChat() {

    const [query, setQuery] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);

    const suggestions = [
        "Explain the architecture of this repository",
        "Which component has the highest impact score?",
        "Show critical dependencies",
        "What are the major architectural smells?",
        "Which module is most risky to modify?"
    ];

    const askQuestion = async () => {

        if (!query.trim()) return;

        try {

            setLoading(true);

            const response = await fetch(
                "http://127.0.0.1:8000/ask",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        query
                    })
                }
            );

            const data = await response.json();

            if (data.success) {
                setAnswer(data.answer);
            } else {
                setAnswer(
                    data.error ||
                    "Failed to get answer."
                );
            }

        } catch (error) {

            console.error(error);

            setAnswer(
                "Unable to connect to backend server."
            );

        } finally {

            setLoading(false);

        }
    };

    return (

        <div
            style={{
                width: "100%"
            }}
        >

            {/* Header */}

            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "15px",
                    marginBottom: "25px"
                }}
            >
                <div
                    style={{
                        width: "60px",
                        height: "60px",
                        borderRadius: "16px",
                        background:
                            "linear-gradient(135deg,#2563eb,#3b82f6)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "24px",
                        color: "white"
                    }}
                >
                    <FaRobot />
                </div>

                <div>
                    <h2
                        style={{
                            margin: 0,
                            fontSize: "28px",
                            color: "#f8fafc"
                        }}
                    >
                        Repository AI Assistant
                    </h2>

                    <div
                        style={{
                            color: "#94a3b8",
                            marginTop: "6px",
                            fontSize: "14px"
                        }}
                    >
                        Ask questions about architecture,
                        dependencies, risks and repository structure.
                    </div>
                </div>
            </div>

            {/* Suggestions */}

            <div
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "10px",
                    marginBottom: "20px"
                }}
            >
                {suggestions.map((item) => (
                    <button
                        key={item}
                        onClick={() => setQuery(item)}
                        style={{
                            background: "#111827",
                            border: "1px solid #334155",
                            color: "#94a3b8",
                            padding: "8px 14px",
                            borderRadius: "999px",
                            cursor: "pointer",
                            fontSize: "13px"
                        }}
                    >
                        {item}
                    </button>
                ))}
            </div>

            {/* Input Card */}

            <div
                style={{
                    background: "#111827",
                    border: "1px solid #1e293b",
                    borderRadius: "18px",
                    padding: "24px"
                }}
            >
                <textarea
                    rows="6"
                    value={query}
                    onChange={(e) =>
                        setQuery(
                            e.target.value
                        )
                    }
                    placeholder="Ask anything about the analyzed repository..."
                    style={{
                        width: "100%",
                        background: "#0f172a",
                        border: "1px solid #334155",
                        borderRadius: "12px",
                        padding: "18px",
                        color: "#f8fafc",
                        fontSize: "15px",
                        resize: "vertical",
                        outline: "none",
                        boxSizing: "border-box"
                    }}
                />

                <div
                    style={{
                        display: "flex",
                        justifyContent: "flex-end",
                        marginTop: "18px"
                    }}
                >
                    <button
                        onClick={askQuestion}
                        disabled={loading}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            padding: "12px 22px",
                            borderRadius: "10px",
                            border: "none",
                            cursor: "pointer",
                            background:
                                loading
                                    ? "#334155"
                                    : "#2563eb",
                            color: "white",
                            fontWeight: "600",
                            fontSize: "14px"
                        }}
                    >
                        {
                            loading
                                ? <FaSpinner />
                                : <FaPaperPlane />
                        }

                        {
                            loading
                                ? "Thinking..."
                                : "Ask Assistant"
                        }
                    </button>
                </div>
            </div>

            {/* Answer */}

            {(loading || answer) && (
                <div
                    style={{
                        marginTop: "25px",
                        background: "#111827",
                        border: "1px solid #1e293b",
                        borderRadius: "18px",
                        padding: "24px"
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            marginBottom: "20px",
                            color: "#38bdf8",
                            fontWeight: "600"
                        }}
                    >
                        <FaBrain />
                        AI Response
                    </div>

                    {
                        loading ? (
                            <div
                                style={{
                                    color: "#94a3b8"
                                }}
                            >
                                Analyzing repository context and
                                generating response...
                            </div>
                        ) : (
                            <div
                                style={{
                                    color: "#e2e8f0",
                                    lineHeight: "1.8",
                                    whiteSpace: "pre-wrap",
                                    fontSize: "15px"
                                }}
                            >
                                {answer}
                            </div>
                        )
                    }
                </div>
            )}

        </div>
    );
}