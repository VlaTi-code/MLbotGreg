from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)  # Уникальный идентификатор пользователя
    username = Column(String, unique=True, nullable=False)  # Имя пользователя
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата регистрации


class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(BigInteger, primary_key=True)  # Уникальный идентификатор плана
    name = Column(String, nullable=False)  # Название тарифа
    description = Column(String, nullable=True)  # Описание плана
    price = Column(DECIMAL(10, 2), nullable=False)  # Цена
    plan_type = Column(Enum('interior', 'dress_up', name='plan_type_enum'), nullable=False)  # Тип плана


class UserPlan(Base):
    __tablename__ = 'user_plans'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)  # Связь с пользователем
    plan_id = Column(BigInteger, ForeignKey('plans.plan_id'), nullable=False)  # Связь с планом
    start_date = Column(DateTime, nullable=False)  # Дата начала действия
    end_date = Column(DateTime, nullable=False)    # Дата окончания действия
    is_active = Column(Boolean, default=True)      # Активен ли план


class UserModel(Base):
    __tablename__ = 'user_models'
    model_id = Column(String, primary_key=True)    # Уникальный идентификатор модели
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)  # Связь с пользователем
    model_name = Column(String, nullable=False)    # Название модели
    model_type = Column(Enum('interior', 'dress_up', name='plan_type_enum'), nullable=False)  # Тип модели
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания модели
