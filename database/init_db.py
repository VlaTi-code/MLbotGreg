import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from core import config
from db_models import Base, Plan


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
    return engine


def create_plans(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    # Тарифные планы для первого сценария (interior)
    interior_plans = [
        Plan(name="Interior Basic", description="1 обучений модели + 5 генераций в месяц",
             price=0.00, plan_type='interior', training_limit=1, generation_limit=5),
        Plan(name="Interior Standard", description="3 обучений модели + 30 генераций в месяц",
             price=2199.00, plan_type="interior", training_limit=3, generation_limit=30),
        Plan(name="Interior Pro", description="5 обучений модели + 50 генераций в месяц",
             price=3199.00, plan_type="interior", training_limit=5, generation_limit=50),
        Plan(name="Interior Premium", description="10 обучений модели + 100 генераций в месяц",
             price=5999.00, plan_type="interior", training_limit=10, generation_limit=100),
    ]

    # Тарифные планы для второго сценария (dress_up)
    dress_up_plans = [
        Plan(name="Dress Up Basic", description="До 20 генераций в месяц",
             price=0.00, plan_type='dress_up', training_limit=None, generation_limit=20),
        Plan(name="Dress Up Standard", description="До 50 генераций в месяц",
             price=700.00, plan_type="dress_up", training_limit=None, generation_limit=50),
        Plan(name="Dress Up Pro", description="До 100 генераций в месяц",
             price=1000.00, plan_type="dress_up", training_limit=None, generation_limit=100),
        Plan(name="Dress Up Premium", description="До 300 генераций в месяц",
             price=2500.00, plan_type="dress_up", training_limit=None, generation_limit=300),
    ]

    # Добавляем планы, если они ещё не существуют
    for plan in interior_plans + dress_up_plans:
        existing_plan = session.query(Plan).filter_by(name=plan.name).first()
        if not existing_plan:
            session.add(plan)
    session.commit()


if __name__ == "__main__":
    create_database()
    engine = create_tables()
    create_plans(engine)
