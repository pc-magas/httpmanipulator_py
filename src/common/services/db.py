from yoyo import read_migrations, get_backend

def apply_migrations(conn):
    backend = get_backend(conn, config={'migration_table': 'migrations'})

    # Read migrations from the 'migrations' folder
    migrations = read_migrations('database/migrations')

    # Apply migrations
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

apply_migrations