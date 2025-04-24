import json
import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Reset tables
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;
''')

# Create tables
cur.executescript('''
CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# Load JSON data
filename = 'roster_data.json'
with open(filename) as f:
    data = json.load(f)

# Insert data
for entry in data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    # Insert User
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Insert Course
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Insert Member
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES (?, ?, ?)''',
        (user_id, course_id, role))

# Save changes
conn.commit()
