from .db_models import Base, User, Plan, UserPlan, UserModel, DailyRequests
from .database import Database

from core import DATABASE_URL

db: Database = Database()
