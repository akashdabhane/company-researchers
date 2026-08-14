import os
import sys
import asyncio
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

# Prepend current directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.database import DATABASE_URL, engine
from app.database.models import Base


async def async_create_database_if_not_exists():
    """
    Asynchronously checks if the target PostgreSQL database exists.
    If it does not exist, connects to the default 'postgres' database
    with AUTOCOMMIT isolation level and executes 'CREATE DATABASE'.
    """
    if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
        print("[DATABASE INIT] Non-PostgreSQL database detected or using SQLite. Skipping CREATE DATABASE.")
        return

    parsed = urlparse(DATABASE_URL)
    db_name = parsed.path.lstrip("/")
    if not db_name:
        db_name = "company_researchers"

    user = parsed.username or os.getenv("POSTGRES_USER", "postgres")
    password = parsed.password or os.getenv("POSTGRES_PASSWORD", "postgres")
    host = parsed.hostname or os.getenv("POSTGRES_HOST", "localhost")
    port = parsed.port or int(os.getenv("POSTGRES_PORT", 5432))

    print(f"[DATABASE INIT] Target database: '{db_name}' on {host}:{port}")

    def _create_db_sync():
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

            # Connect to default system 'postgres' DB to check/create target DB
            conn = psycopg2.connect(
                dbname="postgres",
                user=user,
                password=password,
                host=host,
                port=port,
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            exists = cur.fetchone()

            if not exists:
                print(f"[DATABASE INIT] Database '{db_name}' does not exist. Creating database...")
                # Note: DB name identifier cannot be parameterized in CREATE DATABASE
                cur.execute(f'CREATE DATABASE "{db_name}";')
                print(f"[DATABASE INIT] Database '{db_name}' created successfully!")
            else:
                print(f"[DATABASE INIT] Database '{db_name}' already exists.")

            cur.close()
            conn.close()

        except ImportError:
            print("[DATABASE INIT WARNING] psycopg2 not found. Relying on existing database.")
        except Exception as e:
            print(f"[DATABASE INIT WARNING] Could not verify/create database '{db_name}': {e}")

    # Run in asyncio executor thread for non-blocking execution
    await asyncio.to_thread(_create_db_sync)


def run_alembic_migrations():
    """
    Programmatically runs Alembic migrations ('alembic upgrade head')
    to ensure all database tables and schema modifications are applied.
    """
    try:
        from alembic.config import Config
        from alembic import command

        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alembic.ini")
        alembic_cfg = Config(ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

        print("[ALEMBIC] Applying database migrations ('alembic upgrade head')...")
        command.upgrade(alembic_cfg, "head")
        print("[ALEMBIC] Migrations applied successfully!")

    except Exception as e:
        print(f"[ALEMBIC WARNING] Could not run Alembic migrations automatically: {e}")
        print("[DATABASE INIT] Falling back to SQLAlchemy Base.metadata.create_all...")
        try:
            Base.metadata.create_all(bind=engine)
            print("[DATABASE INIT] Base.metadata.create_all completed successfully.")
        except Exception as ex:
            print(f"[DATABASE ERROR] Base.metadata.create_all fallback failed: {ex}")


async def main():
    print("=" * 60)
    print("[INIT] Running Async Database Creation & Alembic Migration Initialization")
    print("=" * 60)
    await async_create_database_if_not_exists()
    run_alembic_migrations()
    print("=" * 60)
    print("[SUCCESS] Database & Schema Tables Initialization Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
