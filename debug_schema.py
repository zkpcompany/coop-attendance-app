import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()

print(cur.execute("PRAGMA table_info(students);").fetchall())
