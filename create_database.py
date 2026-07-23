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
    start_page INTEGER NOT NULL,
    end_page INTEGER NOT NULL
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
    (chemical_name, start_page, end_page)
    VALUES (?, ?, ?)
    """,
    (
        chemical["chemical"],
        chemical["start_page"],
        chemical["end_page"]
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