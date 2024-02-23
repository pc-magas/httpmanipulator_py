import pathlib
import re
import os

migrations_path = os.path.join(pathlib.Path(__file__).parent.absolute(),"../../database/migrations")

def extract_first_digit(filename):
    match = re.search(r'^\d+', filename)
    return int(match.group()) if match else float('inf')

def get_file_extension(filename):
    # Split the base name and get the file extension
    _, file_extension = os.path.splitext(filename)
    
    return file_extension.replace(".","")

def execureSqlFile(conn,sqlFile):
    cursor = conn.cursor()
    
    print("Run Sql migration file "+sqlFile)
    
    full_sqlFile = os.path.join(migrations_path,sqlFile)

    with open(full_sqlFile, 'r') as script_file:
        sql_script = script_file.read()
        try:
            conn.execute('BEGIN')
            cursor.executescript(sql_script)
            cursor.execute("INSERT INTO migrations(migration_filename) VALUES (?)",[(sqlFile)])
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()

def executeSqlInPythonScript(conn,pythonScript):
    print("execute "+pythonScript)
    return


def createMigrationsTable(conn):
    mig_table_sql="""
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        migration_filename TEXT NOT NULL
    );
"""
    try:
        cursor = conn.cursor()
        conn.execute('BEGIN')
        cursor.execute(mig_table_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()

def apply_migrations(conn):
    files = os.listdir(migrations_path)
    sorted_files = sorted(files, key=extract_first_digit)

    createMigrationsTable(conn)
    
    sql = "SELECT * from migrations where migration_filename = ? LIMIT 1"
    cur = conn.cursor()

    for filename in sorted_files:
        
        res = cur.execute(sql,[(filename)])
        filename_in_db = res.fetchone()

        if filename_in_db is not None:
            print("Skipping Execution of "+filename)
            continue

        ext = get_file_extension(filename)
        if ext == 'sql':
            execureSqlFile(conn,filename)
        elif ext == "py":
            executeSqlInPythonScript(conn,filename)

apply_migrations