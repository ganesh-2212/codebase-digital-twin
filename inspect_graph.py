import pickle

with open("data/dependency_graph.pkl", "rb") as f:
    graph = pickle.load(f)

print("Total nodes:", len(graph.nodes()))
print(list(graph.nodes())[:30])