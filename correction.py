import sqlite3 as sql


db = sql.connect("database.db")
cursor = db.cursor()

for report in cursor.execute(f"SELECT * FROM reports WHERE partner='AlessandroBets'"):
    cursor.execute(f"UPDATE reports SET id='-1002146867266:{report[0].split(':')[1]}' WHERE id='{report[0]}'")

db.commit()
db.close()