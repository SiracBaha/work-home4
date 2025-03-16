import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

db_path = os.getenv('DB_PATH')

# Connect to the SQLite database and create a cursor
con = sqlite3.connect(db_path, check_same_thread=False)
cur = con.cursor()

def execute_query(query):
    """Executes a query and returns the results."""
    cur.execute(query)
    return cur.fetchall()



