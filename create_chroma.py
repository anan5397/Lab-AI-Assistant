import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Connect SQLite
conn = sqlite3.connect(
    "hazcard.db"
)

cursor = conn.cursor()


cursor.execute(
    """
    SELECT 
        id,
        chemical_name,
        start_page,
        end_page
    FROM chemicals
    """
)


rows = cursor.fetchall()


# Create Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="cleapss"
)


for row in rows:

    chemical_id = row[0]
    chemical_name = row[1]
    start_page = row[2]
    end_page = row[3]


    # Convert text into vector

    embedding = model.encode(
        chemical_name
    ).tolist()


    collection.add(

        ids=[
            str(chemical_id)
        ],


        embeddings=[
            embedding
        ],

        metadatas=[
            {
                "chemical": chemical_name,
                "start_page": start_page,
                "end_page": end_page
            }
        ]
    )


print("ChromaDB created")