from fastapi import APIRouter
from analysis.refactoring_advisor import RefactoringAdvisor

router = APIRouter()


@router.get("/refactoring-advice")
def get_refactoring_advice():

    advisor = RefactoringAdvisor()

    recommendations = advisor.generate_advice()

    return {
        "success": True,
        "count": len(recommendations),
        "recommendations": recommendations
    }