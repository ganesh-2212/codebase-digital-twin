from retrieval.graphrag_retrieval import GraphRAGRetriever

retriever = GraphRAGRetriever()

results = retriever.retrieve(
    "How does APIRouter compose routes internally?",
    top_k=5
)

print("\nRESULT COUNT:", len(results))

for r in results:
    print("\n----------------")
    print(r)