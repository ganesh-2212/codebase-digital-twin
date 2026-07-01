from fastapi import APIRouter
from analysis.architecture_impact import ArchitectureImpactAnalyzer

router = APIRouter()


def safe_analyzer():
    try:
        return ArchitectureImpactAnalyzer()
    except:
        return None


@router.get("/architecture_heatmap")
def architecture_heatmap():

    analyzer = safe_analyzer()

    if not analyzer:
        return {
            "success": False,
            "message": "Run /analyze-repository first"
        }

    summaries = analyzer.load_summaries()

    result = []

    for component in summaries:

        analysis = analyzer.analyze(component["name"])

        if analysis:

            result.append({
                "name": analysis["name"],
                "impact_score": analysis["impact_score"],
                "impact_level": analysis["impact_level"]
            })

    return result