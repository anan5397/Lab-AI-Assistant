import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer
import json

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
        aliases,
        chemical_group,
        hazcard,
        start_page,
        end_page,
        molecular_weight
    FROM chemicals
    """
)


rows = cursor.fetchall()


# Create Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

try:
    client.delete_collection("cleapss")
except:
    pass

collection = client.get_or_create_collection(
    name="cleapss"
)

collection = client.get_or_create_collection(
    name="cleapss"
)


for row in rows:

    chemical_id = row[0]
    chemical_name = row[1]
    aliases = json.loads(row[2])
    chemical_group = row[3]
    hazcard = row[4]
    start_page = row[5]
    end_page = row[6]
    molecular_weight = row[7]


    # Convert text into vector
    text = f"""
    Chemical: {chemical_name}

    Aliases:
    {", ".join(aliases)}

    Chemical Group:
    {chemical_group}

    Hazcard:
    {hazcard}
    """

    embedding = model.encode(text).tolist()
 


    collection.add(
    ids=[str(chemical_id)],

    embeddings=[embedding],

    documents=[text],

    metadatas=[
        {
            "chemical": chemical_name,
            "chemical_group": chemical_group,
            "hazcard": hazcard,
            "start_page": start_page,
            "end_page": end_page,
            "molecular_weight": molecular_weight
        }
    ]
)


print("ChromaDB created")
print(collection.count())
conn.close()
