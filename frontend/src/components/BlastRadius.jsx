import { useState } from "react";

export default function BlastRadius() {

    const [component, setComponent] = useState("");
    const [result, setResult] = useState(null);

    const analyze = async () => {

        const response = await fetch(
            `http://localhost:8000/blast-radius?component=${component}`
        );

        const data = await response.json();

        setResult(data);
    };

    return (
        <div>

            <h2>Blast Radius Analysis</h2>

            <input
                value={component}
                onChange={(e) => setComponent(e.target.value)}
                placeholder="backend/routes/chat.py"
            />

            <button onClick={analyze}>
                Analyze
            </button>

            {result && (
                <div>

                    <h3>
                        Risk: {result.risk}
                    </h3>

                    <p>
                        Blast Radius:
                        {" "}
                        {result.blast_radius}
                    </p>

                    <h4>
                        Direct Impact
                    </h4>

                    <ul>
                        {result.direct_impact.map(
                            item => (
                                <li key={item}>
                                    {item}
                                </li>
                            )
                        )}
                    </ul>

                    <h4>
                        Indirect Impact
                    </h4>

                    <ul>
                        {result.indirect_impact.map(
                            item => (
                                <li key={item}>
                                    {item}
                                </li>
                            )
                        )}
                    </ul>

                </div>
            )}

        </div>
    );
}