import chromadb
from sentence_transformers import SentenceTransformer
import fitz

# Start with no model loaded.
# This lets FastAPI start quickly on Render.
model = None


def get_embedding_model():
    global model

    # Load the model only the first time we actually need it.
    if model is None:
        print("Loading SentenceTransformer model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


# Connect to the persistent ChromaDB database.
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Get the existing CLEAPSS collection.
collection = client.get_collection(
    name="cleapss"
)

# Open the Hazcard PDF.
pdf = fitz.open("hazcard.pdf")


def retrieve_context(test_question):

    # Load the embedding model only when a question is actually asked.
    embedding_model = get_embedding_model()

    # Convert the user's question into an embedding vector.
    query_embedding = embedding_model.encode(
        test_question
    ).tolist()

    # Search ChromaDB for the three most similar chunks.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Take the metadata from the closest result.
    best = results["metadatas"][0][0]

    start_page = best["start_page"]
    end_page = best["end_page"]

    context = ""

    # Extract the relevant pages from the PDF.
    for page_num in range(start_page - 1, end_page):

        page = pdf.load_page(page_num)

        context += f"\n========== PAGE {page_num + 1} ==========\n"

        context += page.get_text(
            "text",
            sort=True
        )

        context += "\n"

    print("Extracted text: ", context)

    return context
