from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey, Enum, DECIMAL, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)  # Уникальный идентификатор пользователя
    username = Column(String, unique=True, nullable=False)  # Имя пользователя
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата регистрации


class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(BigInteger, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String, nullable=False)                              # Название плана
    description = Column(String, nullable=True)                        # Описание плана
    price = Column(DECIMAL(10, 2), nullable=False)                     # Цена
    plan_type = Column(Enum('interior', 'dress_up', name='plan_type_enum'), nullable=False)  # Тип плана
    training_limit = Column(Integer, nullable=True)                    # Лимит на обучение моделей
    generation_limit = Column(Integer, nullable=True)                  # Лимит на генерацию изображений


class UserPlan(Base):
    __tablename__ = 'user_plans'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)  # Связь с пользователем
    plan_id = Column(BigInteger, ForeignKey('plans.plan_id'), nullable=False)  # Связь с планом
    start_date = Column(DateTime, nullable=False)  # Дата начала действия
    end_date = Column(DateTime, nullable=False)    # Дата окончания действия
    is_active = Column(Boolean, default=True)      # Активен ли план


class UserModel(Base):
    __tablename__ = 'user_models'
    model_id = Column(BigInteger, primary_key=True, autoincrement=True)    # Уникальный идентификатор модели
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)  # Связь с пользователем
    model_name = Column(String, nullable=False)    # Название модели
    model_type = Column(Enum('interior', 'dress_up', name='plan_type_enum'), nullable=False)  # Тип модели
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания модели
    files_id = Column(String, nullable=False)


class MonthlyRequests(Base):
    __tablename__ = 'monthly_requests'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    model_type = Column(Enum('interior', 'dress_up', name='plan_type_enum'), nullable=False)
    request_type = Column(Enum('learning', 'generation', name='request_type_enum'), nullable=False)