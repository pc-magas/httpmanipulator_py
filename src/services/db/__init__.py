import sqlite3
import os
import pathlib

from services.db.migrations import MigrationRunner 

migrations_path = os.path.join(pathlib.Path(__file__).parent.absolute(),"../../database/migrations")


def create_db(conn_url):

    print("Connecting "+conn_url)
    conn = sqlite3.connect(conn_url)
    conn.row_factory = sqlite3.Row
    print("Setting Up DB")
    runner = MigrationRunner(conn,migrations_path)
    runner.apply_migrations()
    
    return conn

create_db
