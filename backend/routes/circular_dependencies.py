from fastapi import APIRouter
from analysis.circular_dependency_detector import CircularDependencyDetector

router = APIRouter()


@router.get("/circular-dependencies")
def circular_dependencies():

    detector = CircularDependencyDetector()

    result = detector.detect_cycles()

    return {
        "success": True,
        "count": result["count"],
        "cycles": result["cycles"]
    }