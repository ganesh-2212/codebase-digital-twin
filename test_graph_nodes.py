import pickle

with open(
    "data/call_graph.pkl",
    "rb"
) as f:

    graph = pickle.load(f)

print("Keys:")
print(graph.keys())

print("\nTotal nodes:")
print(len(graph["nodes"]))

print("\nTotal edges:")
print(len(graph["edges"]))

print("\nFirst 10 nodes:\n")

for node in graph["nodes"][:10]:
    print(node)

print("\nFirst 10 edges:\n")

for edge in graph["edges"][:10]:
    print(edge)