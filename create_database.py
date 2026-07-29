import sqlite3
import json

# -----------------------------
# Connect to (or create) SQLite database
# -----------------------------
connection = sqlite3.connect("hazcard.db")

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# -----------------------------
# Create the chemicals table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS chemicals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chemical_name TEXT NOT NULL UNIQUE,
    aliases TEXT,
    chemical_group TEXT,
    hazcard TEXT,
    start_page INTEGER NOT NULL,
    end_page INTEGER NOT NULL,
    molecular_weight REAL
)
""")

# -----------------------------
# Open the JSON file
# -----------------------------
with open("cleapss.json", "r") as file:
    chemicals = json.load(file)

# -----------------------------
# Insert each chemical into SQLite
# -----------------------------
for chemical in chemicals:

    cursor.execute("""
    INSERT INTO chemicals
    (chemical_name, aliases, chemical_group, hazcard, start_page, end_page, molecular_weight)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        chemical["chemical_name"],
        json.dumps(chemical["aliases"]),
        chemical["chemical_group"],
        chemical["hazcard"],
        chemical["start_page"],
        chemical["end_page"],
        chemical["molecular_weight"]
    ))

# -----------------------------
# Save changes
# -----------------------------
connection.commit()

# -----------------------------
# Close database
# -----------------------------
connection.close()

print("Database created successfully!")