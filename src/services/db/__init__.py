import sqlite3
from services.db.migrations import apply_migrations 

def create_db(conn_url):

    print("Connecting "+conn_url)
    conn = sqlite3.connect(conn_url)
    print("Setting Up DB")
    apply_migrations(conn)
    
    return conn

create_db
