import sqlite3


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('sentences.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


# Function to create the sentences table if not exists
def create_table(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS sentences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sentence TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)


def get_sentences_from_database():
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sentence FROM sentences")
    sentences = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sentences
