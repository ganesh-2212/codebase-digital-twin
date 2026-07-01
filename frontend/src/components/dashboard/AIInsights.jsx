import React from "react";

export default function AIInsights({
    refactoringCount,
    blastRadiusCount,
    criticalCount,
    changePredictionCount,
}) {
    return (
        <div className="card p-6">
            <h2 className="text-xl font-bold mb-4">
                AI Insights
            </h2>

            <ul className="space-y-3">
                <li>Refactoring Advice: {refactoringCount}</li>
                <li>Critical Components: {criticalCount}</li>
                <li>Blast Radius Analysis: {blastRadiusCount}</li>
                <li>Change Predictions: {changePredictionCount}</li>
            </ul>
        </div>
    );
}