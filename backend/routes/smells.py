from fastapi import APIRouter
from analysis.smell_detector import SmellDetector

router = APIRouter()


@router.get("/smells")
def smells():

    detector = SmellDetector()

    return {
        "success": True,
        "smells":
            detector.detect()
    }