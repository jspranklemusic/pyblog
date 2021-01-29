import sqlite3

conn = sqlite3.connect('database.db')



postsTable="""
     CREATE TABLE posts(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        content LONGTEXT NOT NULL,
        user VARCHAR(255) NOT NULL
    )
"""

usersTable="""
     CREATE TABLE users(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) UNIQUE NOT NULL ,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
"""

conn.execute(postsTable)

# print(conn.cursor().execute("SELECT * FROM users").fetchall())
print("Modified database successfully")
conn.close()