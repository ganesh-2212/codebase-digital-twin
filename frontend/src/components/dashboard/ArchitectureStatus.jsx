import React from "react";

export default function ArchitectureStatus({
    circularDependencies,
    smells,
    healthGrade,
    violations,
}) {
    return (
        <div className="card p-6">
            <h2 className="text-xl font-bold mb-4">
                Architecture Status
            </h2>

            <div className="space-y-3">
                <p>Circular Dependencies: {circularDependencies}</p>
                <p>Architecture Smells: {smells}</p>
                <p>Layer Violations: {violations}</p>
                <p>Health Grade: {healthGrade}</p>
            </div>
        </div>
    );
}