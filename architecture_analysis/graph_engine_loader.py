import pickle


def load_graph():

    with open("data/dependency_graph.pkl", "rb") as f:
        graph = pickle.load(f)

    return graph