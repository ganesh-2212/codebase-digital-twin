import pickle

with open("data/dependency_graph.pkl", "rb") as f:
    graph = pickle.load(f)

print(type(graph))