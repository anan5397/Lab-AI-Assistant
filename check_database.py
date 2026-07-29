import sqlite3
import json

connection = sqlite3.connect("hazcard.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM chemicals")

rows = cursor.fetchall()

for row in rows:

    # Convert JSON string back into a Python list
    aliases = json.loads(row[2])

    print(f"""
ID: {row[0]}
Chemical: {row[1]}
Aliases: {", ".join(aliases)}
Chemical Group: {row[3]}
Hazcard: {row[4]}
Start Page: {row[5]}
End Page: {row[6]}
Molecular Weight: {row[7]}
--------------------------
""")

connection.close()