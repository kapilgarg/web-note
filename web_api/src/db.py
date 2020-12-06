"""
TODO
"""
import sqlite3
import os
import datetime


DATABASE = "highlighter.db"

def connection():
    return sqlite3.connect(DATABASE)


def save(data):
    conn = connection()
    
    created_on = datetime.datetime.utcnow() if 'id' not in data else data.get('created_on')
    modified_on = datetime.datetime.utcnow()

    sql = ''' INSERT INTO note(user_id, note, source, tags,created_on,modified_on)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    n = (data.get('user_id'),
         data.get('text'),
         data.get('source'),
         data.get('tags'),
         created_on,
         modified_on)

    cur.execute(sql, n)
    conn.commit()

def get_all(limit, offset):
    query = f"select * from note order by modified_on desc limit {limit} offset {offset}"
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def get(note_id):
    query = f"select * from note where id = {note_id}"
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def init_db():
    connection = sqlite3.connect(DATABASE)
    base_dir =os.path.dirname(__file__)

    with open(os.path.join(base_dir,'schema.sql')) as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()