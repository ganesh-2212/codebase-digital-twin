import pickle

with open(
    "data/architecture_summaries.pkl",
    "rb"
) as f:

    data = pickle.load(f)

print(f"Total summaries: {len(data)}\n")

for item in data[:10]:

    print(item)

    print("-" * 50)