from fastapi import APIRouter
from analysis.architecture_impact import ArchitectureImpactAnalyzer

router = APIRouter()


def safe_load_analyzer():
    try:
        return ArchitectureImpactAnalyzer()
    except Exception as e:
        print("Analyzer not ready:", e)
        return None


@router.get("/component/{component_name}")
def get_component_details(component_name: str):

    analyzer = safe_load_analyzer()

    if analyzer is None:
        return {
            "success": False,
            "message": "Run /analyze-repository first"
        }

    architecture_info = analyzer.analyze(component_name)

    if not architecture_info:
        return {
            "success": False,
            "message": "Component not found"
        }

    return {
        "success": True,
        "name": architecture_info["name"],
        "type": architecture_info["type"],
        "file": architecture_info["file"],
        "methods": architecture_info["methods"],
        "calls": architecture_info["calls"],
        "impact_score": architecture_info["impact_score"],
        "impact_level": architecture_info["impact_level"]
    }