import sqlite3

# Create or open the database file
conn = sqlite3.connect("hazcard.db")

# Create something that can execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chemicals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chemical_name TEXT NOT NULL,
    page_number INTEGER NOT NULL
)
""")

# Save changes
conn.commit()

# Close the database
conn.close()

print("Database created!")