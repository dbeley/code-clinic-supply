from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import engine

from main import User, Tweet # SQLAlchemy model


app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]

class TweetAdmin(ModelView, model=Tweet):
    column_list = [User.id, User.name]

admin.add_view(UserAdmin)
admin.add_view(TweetAdmin)
