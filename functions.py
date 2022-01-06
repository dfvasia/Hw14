import sqlite3


def open_sqlite3(name_db, query):
	with sqlite3.connect(name_db) as connection:
		cursor = connection.cursor()
		cursor.execute(query)
		return cursor.fetchall()
