import chromadb
from sentence_transformers import SentenceTransformer
import fitz

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

test_question = "Can I heat Barium metal?"

query_embedding = model.encode(    #Does the embedding part 
    test_question
).tolist()

results = collection.query(        #Finds answers in the collections (aka the database)
    query_embeddings=[query_embedding],
    n_results=3
)

best = results["metadatas"][0][0]

start_page = best["start_page"]
end_page = best["end_page"]
#print("Best result: ", best)

pdf = fitz.open("hazcard.pdf")
context = ""

for page_num in range(start_page - 1, end_page):

    page = pdf.load_page(page_num)

    context += f"\n========== PAGE {page_num + 1} ==========\n"

    context += page.get_text("text", sort=True) #sort = True ensures that the text is extracted in a logical reading order, which is especially useful for documents with complex layouts or multiple columns.

    context += "\n"

pdf.close()
print("Extracted text: ", context)