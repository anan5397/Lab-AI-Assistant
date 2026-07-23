import chromadb
from sentence_transformers import SentenceTransformer

# Load the same embedding model you used in create_chroma.py
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the existing Chroma database
client = chromadb.PersistentClient(path="./chroma_db")

# Open the collection
collection = client.get_collection(name="cleapss")


def search_chroma(question):
    # Convert the question into an embedding
    question_embedding = model.encode(question).tolist()

    # Search the collection
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1   #Controls how many results you want to retrieve.
    )

    return results