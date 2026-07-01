from fastapi import APIRouter

from analysis.critical_components import CriticalComponentsAnalyzer

router = APIRouter()


@router.get("/critical-components")
def critical_components():

    analyzer = CriticalComponentsAnalyzer()

    results = analyzer.analyze()

    return {
        "success": True,
        "count": len(results),
        "components": results
    }