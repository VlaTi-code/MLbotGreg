from .db_models import Base, User, Event, Registration, BeerPongTeam
from .database import DataBase

from core import DATABASE_URL

db: DataBase = DataBase(DATABASE_URL)
