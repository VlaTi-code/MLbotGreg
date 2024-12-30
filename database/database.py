import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import create_engine
from sqlalchemy import select, func
from datetime import datetime

from core.config import DATABASE_URL, config
from .db_models import Base, User, Plan, UserPlan, UserModel, MonthlyRequests


plans = {
    "interior_plans": [
        {
            "id": 1,
            "name": "Interior Basic",
            "description": "1 обучений модели + 5 генераций в месяц",
            "price": 0.00,
            "plan_type": "interior",
            "training_limit": 1,
            "generation_limit": 5
        },
        {
            "id": 2,
            "name": "Interior Standard",
            "description": "3 обучений модели + 30 генераций в месяц",
            "price": 2199.00,
            "plan_type": "interior",
            "training_limit": 3,
            "generation_limit": 30
        },
        {
            "id": 3,
            "name": "Interior Pro",
            "description": "5 обучений модели + 50 генераций в месяц",
            "price": 3199.00,
            "plan_type": "interior",
            "training_limit": 5,
            "generation_limit": 50
        },
        {
            "id": 4,
            "name": "Interior Premium",
            "description": "10 обучений модели + 100 генераций в месяц",
            "price": 5999.00,
            "plan_type": "interior",
            "training_limit": 10,
            "generation_limit": 100
        }
    ],
    "dress_up_plans": [
        {
            "id": 5,
            "name": "Dress Up Basic",
            "description": "До 20 генераций в месяц",
            "price": 0.00,
            "plan_type": "dress_up",
            "training_limit": None,
            "generation_limit": 20
        },
        {
            "id": 6,
            "name": "Dress Up Standard",
            "description": "До 50 генераций в месяц",
            "price": 700.00,
            "plan_type": "dress_up",
            "training_limit": None,
            "generation_limit": 50
        },
        {
            "id": 7,
            "name": "Dress Up Pro",
            "description": "До 100 генераций в месяц",
            "price": 1000.00,
            "plan_type": "dress_up",
            "training_limit": None,
            "generation_limit": 100
        },
        {
            "id": 8,
            "name": "Dress Up Premium",
            "description": "До 300 генераций в месяц",
            "price": 2500.00,
            "plan_type": "dress_up",
            "training_limit": None,
            "generation_limit": 300
        }
    ]
}


class Database:
    def __init__(self):
        self.async_engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для отладки
        self.async_session = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        self.sync_engine = create_engine(
            f"postgresql+psycopg2://{config.database.user}:{config.database.password}"
            f"@{config.database.host}:{config.database.port}/{config.database.name}"
        )

    def create_database(self):
        """
        Создаёт базу данных, если она не существует.
        """
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

    async def create_tables(self):
        """
        Создаёт таблицы в базе данных.
        """
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы.")

    def create_plans(self):
        """
        Заполняет таблицу тарифных планов, если планы ещё не добавлены.
        """
        Session = sessionmaker(bind=self.sync_engine)
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
        try:
            for plan in interior_plans + dress_up_plans:
                existing_plan = session.query(Plan).filter_by(name=plan.name).first()
                if not existing_plan:
                    session.add(plan)
            session.commit()
            print("Тарифные планы успешно добавлены.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении тарифных планов: {e}")
        finally:
            session.close()

    async def initialize(self):
        """
        Полная инициализация базы данных:
        - Создание базы данных
        - Создание таблиц
        - Заполнение тарифных планов
        """
        self.create_database()  # Создаёт базу данных (синхронно)
        await self.create_tables()  # Создаёт таблицы (асинхронно)
        self.create_plans()  # Заполняет таблицу тарифных планов (синхронно)
        print("Инициализация базы данных завершена.")

    async def get_user_id_by_username(self, username: str):
        """
        Получить user_id по username.

        :param username: имя пользователя в Telegram.
        :return: user_id или None, если пользователь не найден.
        """
        async with self.async_session() as session:
            try:
                print(f"Ищу пользователя с username: {username.strip()}")
                result = await session.execute(
                    select(User).filter(func.lower(User.username) == username.lower().strip())
                )
                user = result.scalars().first()

                if user:
                    print(f"Найден пользователь {username} с ID {user.user_id}.")
                    return user.user_id
                else:
                    print(f"Пользователь с именем {username} не найден.")
                    return None
            except Exception as e:
                print(f"Ошибка при получении user_id для пользователя {username}: {e}")
                return None

    async def add_user(self, username: str):
        """
        Асинхронное добавление нового пользователя в базу данных.

        :param username: имя пользователя в Telegram.
        """
        async with self.async_session() as session:
            try:
                result = await session.execute(select(User).filter_by(username=username))
                existing_user = result.scalars().first()
                if existing_user:
                    print(f"Пользователь {username} уже существует.")
                    return existing_user

                new_user = User(username=username)
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)

                from datetime import datetime, timedelta
                start_date = datetime.utcnow()
                end_date = start_date + timedelta(days=30)

                new_user_plan_1 = UserPlan(
                    user_id=new_user.user_id,
                    plan_id=plans["interior_plans"][0]["id"],
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                )
                new_user_plan_2 = UserPlan(
                    user_id=new_user.user_id,
                    plan_id=plans["dress_up_plans"][0]["id"],
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                )
                session.add_all([new_user_plan_1, new_user_plan_2])
                await session.commit()
                print(f"Пользователь {username} успешно добавлен с ID {new_user.user_id}.")

                return new_user

            except Exception as e:
                await session.rollback()
                print(f"Ошибка при добавлении пользователя: {e}")

    async def add_model(self, user_id: int, model_name: str, model_type: str, files_id: str):
        """
        Добавление новой модели в базу данных.

        :param user_id: ID пользователя, владеющего моделью.
        :param model_name: Название модели.
        :param model_type: Тип модели ('interior' или 'dress_up').
        :param files_id: Идентификаторы файлов, связанных с моделью.
        """
        async with self.async_session() as session:
            try:
                result = await session.execute(select(User).filter_by(user_id=user_id))
                user = result.scalars().first()

                if not user:
                    print(f"Пользователь с ID {user_id} не найден.")
                    return None

                new_model = UserModel(
                    user_id=user_id,
                    model_name=model_name,
                    model_type=model_type,
                    files_id=files_id
                )

                session.add(new_model)
                await session.commit()

                await session.refresh(new_model)

                print(f"Модель '{model_name}' успешно добавлена для пользователя {user_id}.")
                return new_model

            except Exception as e:
                await session.rollback()
                print(f"Ошибка при добавлении модели: {e}")

    async def get_models_by_user_id(self, user_id: int) -> list[str]:
        """
        Получить список всех model_name по user_id.

        :param user_id: ID пользователя.
        :return: Список названий моделей (model_name).
        """
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel.model_name).filter_by(user_id=user_id)
                )
                rows = result.all()

                models = [row[0] for row in rows]

                print(f"Найдено {len(models)} моделей для пользователя с ID {user_id}.")
                return models

            except Exception as e:
                print(f"Ошибка при получении моделей для пользователя {user_id}: {e}")
                return []


    async def get_user_requests_count(self, user_id: int) -> dict:
        """
        Возвращает количество запросов по каждому типу (learning / generation)
        для обоих model_type (interior / dress_up) пользователя с заданным user_id.

        Пример структуры возвращаемого словаря:
        {
          "interior": {
            "learning": 3,
            "generation": 10
          },
          "dress_up": {
            "learning": 0,
            "generation": 5
          }
        }
        """
        async with self.async_session() as session:
            result = await session.execute(
                select(
                    MonthlyRequests.model_type,
                    MonthlyRequests.request_type,
                    func.count()
                )
                .where(MonthlyRequests.user_id == user_id)
                .group_by(MonthlyRequests.model_type, MonthlyRequests.request_type)
            )
            rows = result.all()

        summary = {
            "interior": {
                "learning": 0,
                "generation": 0
            },
            "dress_up": {
                "learning": 0,
                "generation": 0
            }
        }

        for (model_type, request_type, count_val) in rows:
            if model_type == "interior":
                if request_type == "learning":
                    summary["interior"]["learning"] += count_val
                elif request_type == "generation":
                    summary["interior"]["generation"] += count_val

            elif model_type == "dress_up":
                if request_type == "learning":
                    summary["dress_up"]["learning"] += count_val
                elif request_type == "generation":
                    summary["dress_up"]["generation"] += count_val

        return summary

    async def add_request(self, user_id: int, model_type: str, request_type: str):
        """
        Добавить новую запись (обращение) в таблицу monthly_requests.

        :param user_id: идентификатор пользователя
        :param model_type: 'interior' или 'dress_up'
        :param request_type: 'learning' или 'generation'
        """
        async with self.async_session() as session:
            try:
                new_request = MonthlyRequests(
                    user_id=user_id,
                    model_type=model_type,
                    request_type=request_type,
                    date=datetime.utcnow()  # Можно не указывать явно, т.к. есть default= в модели
                )
                session.add(new_request)
                await session.commit()
                await session.refresh(new_request)

                print(f"Новая запись в monthly_requests: user_id={user_id}, "
                      f"model_type={model_type}, request_type={request_type}")
                return new_request
            except Exception as e:
                await session.rollback()
                print(f"Ошибка при добавлении записи в monthly_requests: {e}")

    async def get_user_request_count(self, user_id: int) -> dict:
        """
        Возвращает количество запросов по каждому типу (learning / generation)
        для обоих model_type (interior / dress_up) пользователя с заданным user_id.

        Пример структуры:
        {
          "interior": {
            "learning": 3,
            "generation": 10
          },
          "dress_up": {
            "learning": 0,
            "generation": 5
          }
        }
        """
        async with self.async_session() as session:
            # Группируем по model_type и request_type
            result = await session.execute(
                select(
                    MonthlyRequests.model_type,
                    MonthlyRequests.request_type,
                    func.count()
                )
                .where(MonthlyRequests.user_id == user_id)
                .group_by(MonthlyRequests.model_type, MonthlyRequests.request_type)
            )
            rows = result.all()

        # Заранее формируем структуру для счётчиков
        summary = {
            "interior": {
                "learning": 0,
                "generation": 0
            },
            "dress_up": {
                "learning": 0,
                "generation": 0
            }
        }

        # Заполняем словарь по полученным данным
        for (model_type, request_type, count_val) in rows:
            if model_type == "interior":
                if request_type == "learning":
                    summary["interior"]["learning"] += count_val
                elif request_type == "generation":
                    summary["interior"]["generation"] += count_val

            elif model_type == "dress_up":
                if request_type == "learning":
                    summary["dress_up"]["learning"] += count_val
                elif request_type == "generation":
                    summary["dress_up"]["generation"] += count_val

        return summary

    async def get_user_plan_limits(self, user_id: int) -> dict:
        """
        Возвращает суммарные лимиты по обучению (training_limit) и генерации (generation_limit)
        для обоих model_type ('interior' и 'dress_up') у заданного user_id,
        НЕ вычитая уже израсходованное.

        Пример возвращаемой структуры:
        {
          "interior": {
            "learning": 0,      # Или любое суммарное число
            "generation": 0
          },
          "dress_up": {
            "learning": 0,
            "generation": 0
          }
        }

        Если планов нужного типа нет, значения будут по умолчанию 0.
        """

        async with self.async_session() as session:
            now = datetime.utcnow()

            # Получаем все активные планы пользователя
            # При необходимости можно убрать проверку дат (start_date, end_date),
            # если не учитывается срок действия.
            stmt = (
                select(
                    Plan.plan_type,
                    Plan.training_limit,
                    Plan.generation_limit
                )
                .join(UserPlan, Plan.plan_id == UserPlan.plan_id)
                .where(
                    UserPlan.user_id == user_id,
                    UserPlan.is_active == True,
                    UserPlan.start_date <= now,
                    UserPlan.end_date >= now
                )
            )
            result = await session.execute(stmt)
            rows = result.all()

        # Готовим структуру для суммирования
        plan_summary = {
            "interior": {
                "learning": 0,
                "generation": 0
            },
            "dress_up": {
                "learning": 0,
                "generation": 0
            }
        }

        # Складываем лимиты по каждому плану
        for (plan_type, training_limit, generation_limit) in rows:
            # Если поля None, подставим 0
            tlim = training_limit if training_limit is not None else 0
            glim = generation_limit if generation_limit is not None else 0

            plan_summary[plan_type]["learning"] += tlim
            plan_summary[plan_type]["generation"] += glim

        return plan_summary
