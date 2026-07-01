import RepositoryAnalyzer from "../components/RepositoryAnalyzer";
import RepositoryStats from "../components/RepositoryStats";

export default function RepositoryPage({
    analysisComplete,
    repository,
    setAnalysisComplete,
    setRepository
}) {

    return (
        <div>

            <RepositoryAnalyzer
                setAnalysisComplete={
                    setAnalysisComplete
                }
                setRepository={
                    setRepository
                }
            />

            {
                analysisComplete &&
                <>
                    <div
                        style={{
                            padding: "20px",
                            textAlign: "center",
                            fontSize: "18px",
                            fontWeight: "bold"
                        }}
                    >
                        Current Repository

                        <br />

                        <span
                            style={{
                                color: "#38bdf8"
                            }}
                        >
                            {repository}
                        </span>
                    </div>

                    <RepositoryStats />
                </>
            }

        </div>
    );
}