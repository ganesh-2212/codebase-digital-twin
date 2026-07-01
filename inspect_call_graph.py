import pickle
import pprint

with open("data/call_graph.pkl", "rb") as f:
    graph = pickle.load(f)

print("\nTYPE:")
print(type(graph))

print("\nKEYS:")
if isinstance(graph, dict):
    print(graph.keys())

print("\nFIRST 5 NODES:")
pprint.pp(graph.get("nodes", [])[:5])

print("\nFIRST 5 EDGES:")
pprint.pp(graph.get("edges", [])[:5])