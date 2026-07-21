import sqlite3

connection = sqlite3.connect("hazcard.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM chemicals")

rows = cursor.fetchall()

for row in rows:
    print(f"""
ID: {row[0]}
Chemical: {row[1]}
Start Page: {row[2]}
End Page: {row[3]}
--------------------------
""")

connection.close()