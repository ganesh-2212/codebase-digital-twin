import pickle
import chromadb

client = chromadb.PersistentClient(
    path="data/vector_db"
)

collection = client.get_or_create_collection(
    name="codebase_embeddings"
)

with open(
    "data/chunk_embeddings.pkl",
    "rb"
) as f:

    data = pickle.load(f)

documents = data["documents"]
metadatas = data["metadatas"]

ids = []

for i in range(len(documents)):
    ids.append(str(i))

collection.add(

    documents=documents,

    metadatas=metadatas,

    ids=ids

)

print(
    f"Inserted {len(documents)} chunks"
)