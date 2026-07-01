from fastapi import APIRouter
from pydantic import BaseModel

import os

from analysis.repository_digital_twin import (
    RepositoryDigitalTwin
)

router = APIRouter()

# ==========================================
# GLOBAL INSTANCE
# ==========================================

twin = None


# ==========================================
# REQUEST MODEL
# ==========================================

class AskRequest(BaseModel):
    query: str


# ==========================================
# ASK REPOSITORY
# ==========================================

@router.post("/ask")
def ask_repository(request: AskRequest):

    global twin

    try:

        # ----------------------------------
        # CHECK IF ANALYSIS EXISTS
        # ----------------------------------

        required_files = [

            "data/dependency_graph.pkl",
            "data/architecture_clusters.pkl",
            "data/parsed_chunks.json"

        ]

        missing_files = [

            file
            for file in required_files
            if not os.path.exists(file)

        ]

        if missing_files:

            return {

                "success": False,

                "error":
                    "No repository has been analyzed yet. "
                    "Please analyze a repository first.",

                "missing_files":
                    missing_files

            }

        # ----------------------------------
        # LAZY INITIALIZATION
        # ----------------------------------

        if twin is None:

            print(
                "\nInitializing Repository Digital Twin..."
            )

            twin = RepositoryDigitalTwin()

            print(
                "Digital Twin Ready."
            )

        # ----------------------------------
        # ASK QUESTION
        # ----------------------------------

        answer = twin.answer(
            request.query
        )

        return {

            "success": True,

            "query":
                request.query,

            "answer":
                answer

        }

    except Exception as e:

        return {

            "success": False,

            "error":
                str(e)

        }