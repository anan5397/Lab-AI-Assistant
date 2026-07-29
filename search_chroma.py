import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(      #This line creates a persistent ChromaDB client that stores the database in the specified path. The database will be saved in the "chroma_db" directory, allowing for data persistence across sessions.
    path="./chroma_db"
)

collection = client.get_collection(
    name="cleapss"
)

test_question = "Can I heat Aluminium chloride?"

query_embedding = model.encode(    #Does the embedding part 
    test_question
).tolist()

results = collection.query(        #Finds answers in the collections (aka the database)
    query_embeddings=[query_embedding],
    n_results=3
)

best = results["metadatas"][0][0]
print("All results: ", results)
#print("Best result: ", best)
