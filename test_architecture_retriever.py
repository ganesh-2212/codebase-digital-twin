from retrieval.architecture_retriever import (
    ArchitectureRetriever
)

retriever = ArchitectureRetriever()

results = retriever.retrieve(
    "How does APIRouter compose routes internally?"
)

for r in results:

    print(r)

    print("-" * 50)