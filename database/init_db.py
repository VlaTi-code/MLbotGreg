import psycopg2


from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from core import config
from db_models import Base


def create_database():
    connection = psycopg2.connect(
        user=config.database.user,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    try:
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{config.database.name}'")
        if cursor.fetchone():
            print("База данных уже существует.")
        else:
            cursor.execute(f'CREATE DATABASE {config.database.name}')
            print("База данных создана.")
    finally:
        cursor.close()
        connection.close()


def create_tables():
    engine = create_engine(
        f"postgresql+psycopg2://{config.database.user}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.name}"
    )
    Base.metadata.create_all(engine)
    print("Таблицы созданы.")


if __name__ == "__main__":
    create_database()
    create_tables()
