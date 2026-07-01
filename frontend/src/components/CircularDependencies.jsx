import { useEffect, useState } from "react";

export default function CircularDependencies() {

    const [cycles, setCycles] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    useEffect(() => {

        fetch(
            "http://localhost:8000/circular-dependencies"
        )
            .then(
                res => res.json()
            )
            .then(data => {

                setCycles(
                    data.cycles || []
                );

            })
            .finally(() => {

                setLoading(false);

            });

    }, []);

    return (

        <div
            style={{
                padding: "20px"
            }}
        >

            <h1>
                Circular Dependencies
            </h1>

            {
                loading &&
                <p>
                    Loading...
                </p>
            }

            {
                !loading &&
                cycles.length === 0 &&
                <p>
                    No circular dependencies found.
                </p>
            }

            {
                cycles.map(
                    (
                        cycle,
                        index
                    ) => (

                        <div
                            key={index}
                            style={{
                                padding: "20px",
                                marginBottom: "20px",
                                background:
                                    "#1e293b",
                                borderRadius:
                                    "12px"
                            }}
                        >

                            <h3>
                                Cycle {
                                    index + 1
                                }
                            </h3>

                            <p>
                                Length:
                                {" "}
                                {
                                    cycle.length
                                }
                            </p>

                            <div
                                style={{
                                    display:
                                        "flex",
                                    flexWrap:
                                        "wrap",
                                    gap: "10px"
                                }}
                            >

                                {
                                    cycle.cycle.map(
                                        (
                                            node,
                                            i
                                        ) => (

                                            <div
                                                key={
                                                    i
                                                }
                                                style={{
                                                    padding:
                                                        "8px 12px",
                                                    background:
                                                        "#334155",
                                                    borderRadius:
                                                        "8px"
                                                }}
                                            >
                                                {
                                                    node
                                                }
                                            </div>

                                        )
                                    )
                                }

                            </div>

                        </div>

                    )
                )
            }

        </div>

    );
}