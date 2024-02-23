import sqlite3
import pathlib
import re
import os

migrations_path = os.path.join(pathlib.Path(__file__).parent.absolute(),"../database/migrations")

def extract_first_digit(filename):
    match = re.search(r'^\d+', filename)
    return int(match.group()) if match else float('inf')

def get_file_extension(filename):
    # Split the base name and get the file extension
    _, file_extension = os.path.splitext(filename)
    
    return file_extension

def execureSqlFile(conn,sqlFile):
    cursor = conn.cursor()

    print("Run Sql migration file "+sqlFile)

    with open(sqlFile, 'r') as script_file:
        sql_script = script_file.read()
        try:
            conn.execute('BEGIN')
            cursor.executescript(sql_script)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()

def executeSqlInPythonScript(conn,pythonScript):
    print("execute "+pythonScript)
    return

def apply_migrations(conn):
    files = os.listdir(migrations_path)
    sorted_files = sorted(files, key=extract_first_digit)

    cursor = conn.cursor()

    for filename in sorted_files:
        ext = get_file_extension(filename)
        ext = ext.replace(".","")
        filename = os.path.join(migrations_path,filename)
        if ext == 'sql':
            execureSqlFile(conn,filename)
        elif ext == "py":
            executeSqlInPythonScript(conn,filename)

def create_db(conn_url):

    print("Connecting "+conn_url)
    conn = sqlite3.connect(conn_url)
    print("Setting Up DB")
    apply_migrations(conn)
    
    return conn

create_db
