import re
import os
import sys
import importlib

def extract_first_digit(filename):
    match = re.search(r'^\d+', filename)
    return int(match.group()) if match else float('inf')

def get_file_extension(filename):
    # Split the base name and get the file extension
    _, file_extension = os.path.splitext(filename)
        
    return file_extension.replace(".","")

class MigrationRunner:

    def __init__(self,conn,migrations_path):
        self.conn = conn
        self.migrations_path = migrations_path

    def __executeSqlFile(self,sqlFile):
        conn = self.conn
        cursor = conn.cursor()
        
        print("Run Sql migration file "+sqlFile)
        
        full_sqlFile = os.path.join(self.migrations_path,sqlFile)

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

    def __executeSqlInPythonScript(self,pythonScript):

        conn = self.conn
        migrations_path=self.migrations_path

        print("Execute Python Migration "+pythonScript)
        module_name = "database.migrations."+pythonScript.replace(".py","")
        migration_module = importlib.import_module(module_name)

        if hasattr(migration_module, 'up'):
            cursor = conn.cursor()
            try:
                conn.execute('BEGIN')
                migration_module.up(cursor)
                cursor.execute("INSERT INTO migrations(migration_filename) VALUES (?)",[(pythonScript)])
                conn.commit()
            except Exception as e:
                conn.commit()
                raise e
            finally:
                cursor.close()
            print("Execution of " + pythonScript + " completed successfully")
        else:
            raise Exception(f"Error: {pythonScript} does not define a 'up' function")
        
    def __createMigrationsTable(self):
        conn = self.conn

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

    def apply_migrations(self):

        conn = self.conn
        migrations_path = self.migrations_path

        files = os.listdir(migrations_path)
        sorted_files = sorted(files, key=extract_first_digit)

        self.__createMigrationsTable()
        
        sql = "SELECT * from migrations where migration_filename = ? LIMIT 1"
        cur = conn.cursor()

        for filename in sorted_files:

            if(filename == "__init__.py"):
                continue

            res = cur.execute(sql,[(filename)])
            filename_in_db = res.fetchone()

            if filename_in_db is not None:
                print("Skipping Execution of "+filename)
                continue

            ext = get_file_extension(filename)
            if ext == 'sql':
                self.__executeSqlFile(filename)
            elif ext == "py":
                self.__executeSqlInPythonScript(filename)

MigrationRunner