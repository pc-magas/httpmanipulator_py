import re
import os

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

    def __executeSqlInPythonScript(self,pythonScript):

        conn = self.conn
        migrations_path=self.migrations_path
        
        print("Execute Python Migration "+pythonScript)
        try:
            # Import the module dynamically
            full_pythonScript = os.path.join(migrations_path,pythonScript)
            module_name = full_pythonScript.replace(".py","",full_pythonScript)  # Remove the file extension
            migration_module = __import__(module_name)

            # Call the run_migration function (or another named function) from the module
            if hasattr(migration_module, 'run_migration'):
                migration_module.up(conn)
                print("Execution of " + pythonScript + " completed successfully")
            else:
                print(f"Error: {pythonScript} does not define a 'run_migration' function")
        except Exception as e:
            print("Error executing " + pythonScript + ": " + str(e))


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