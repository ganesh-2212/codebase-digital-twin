import React from "react";

export default function RepositoryOverview({ stats }) {
    return (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div className="card">
                <h3>Files</h3>
                <p>{stats.files}</p>
            </div>

            <div className="card">
                <h3>Dependencies</h3>
                <p>{stats.dependencies}</p>
            </div>

            <div className="card">
                <h3>Communities</h3>
                <p>{stats.communities}</p>
            </div>

            <div className="card">
                <h3>Health Score</h3>
                <p>{stats.health}</p>
            </div>

            <div className="card">
                <h3>Critical Components</h3>
                <p>{stats.critical}</p>
            </div>

            <div className="card">
                <h3>Layer Violations</h3>
                <p>{stats.violations}</p>
            </div>
        </div>
    );
}