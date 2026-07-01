from fastapi import APIRouter
from pydantic import BaseModel
import os

from parser_engine.repo_parser import RepoParser
from graph_engine.dependency_graph import DependencyGraphGenerator

from analysis.architecture_summary import (
    ArchitectureSummaryGenerator
)

from analysis.community_detection import (
    CommunityDetector
)

router = APIRouter()


class RepositoryRequest(BaseModel):
    repo_url: str


@router.post("/analyze-repository")
def analyze_repository(request: RepositoryRequest):

    print("\n========== ANALYSIS START ==========")

    # ==========================================
    # CLEAN OLD FILES
    # ==========================================

    files_to_delete = [
        "data/dependency_graph.pkl",
        "data/architecture_clusters.pkl",
        "data/architecture_summaries.pkl",
        "data/parsed_chunks.json",
    ]

    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted old file: {file}")

    # ==========================================
    # STEP 1 - CLONE REPOSITORY
    # ==========================================

    parser = RepoParser(request.repo_url)

    print("STEP 1 - Clone Repository")

    parser.clone_repository()

    # ==========================================
    # STEP 2 - PARSE REPOSITORY
    # ==========================================

    print("STEP 2 - Parse Repository")

    parser.parse_repository()

    # ==========================================
    # STEP 3 - DEPENDENCY GRAPH
    # ==========================================

    print("STEP 3 - Build Dependency Graph")

    graph_generator = DependencyGraphGenerator(
        parser.local_path
    )

    graph_generator.build_graph()
    graph_generator.save_graph()

    nodes_count = len(
        graph_generator.graph.nodes()
    )

    edges_count = len(
        graph_generator.graph.edges()
    )

    print(f"Nodes: {nodes_count}")
    print(f"Edges: {edges_count}")

    # ==========================================
    # STEP 4 - ARCHITECTURE SUMMARIES
    # ==========================================

    print("STEP 4 - Architecture Summaries")

    try:
        summary_generator = (
            ArchitectureSummaryGenerator(
                parser.local_path
            )
        )

        summary_generator.generate()
        summary_generator.save()

        summary_count = len(
            summary_generator.summaries
        )

        print(
            f"Architecture summaries: {summary_count}"
        )

    except Exception as e:

        print(
            f"Architecture summary generation failed: {e}"
        )

        summary_count = 0

    # ==========================================
    # STEP 5 - COMMUNITY DETECTION
    # ==========================================

    print("STEP 5 - Community Detection")

    print("STEP 6 - Layer Detection")

    from analysis.layer_detector import (LayerDetector)

    detector = LayerDetector()

    layers = detector.generate()

    detector.save(layers)

    print(f"Detected {len(layers)} layers")

    

    try:
        detector = CommunityDetector()

        communities = detector.detect()

        detector.save(
            communities
        )

        cluster_count = len(
            communities
        )

        print(
            f"Detected {cluster_count} communities"
        )

    except Exception as e:

        print(
            f"Community detection failed: {e}"
        )

        cluster_count = 0

    print(
        "\n========== ANALYSIS COMPLETE ==========\n"
    )

    return {

        "success": True,

        "repository":
            request.repo_url,

        "repo_path":
            parser.local_path,

        "dependency_nodes":
            nodes_count,

        "dependency_edges":
            edges_count,

        "architecture_summaries":
            summary_count,

        "clusters":
            cluster_count
    }