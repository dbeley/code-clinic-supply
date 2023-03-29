from urllib.request import Request

from fastapi import FastAPI
from sqladmin import Admin, ModelView

import os

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL2 = DATABASE_URL.replace("postgres", "postgresql")

Base = declarative_base()
engine = create_engine(
    DATABASE_URL2,
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(ForeignKey("user.id"))

Base.metadata.create_all(engine)  # Create tables


app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]

class TweetAdmin(ModelView, model=Tweet):
    column_list = [Tweet.id, Tweet.content]


admin.add_view(UserAdmin)
admin.add_view(TweetAdmin)

@app.get("/")
async def root():
    return {"message": "Hello World"}\

Session = sessionmaker(bind=engine)
session = Session()

# @app.get("/tweets/")
# async def read_items() -> list[Tweet]:
#     tweets = session.query(Tweet).all()
#     return [tweet.__dict__ for tweet in tweets]

# @app.get(
#     "/tweets/{item_id}/content",
#     response_model=Tweet,
#     response_model_include=["content"],
# )
# async def read_tweet_name(tweet_id: str):
#     tweets = session.query(Tweet).all()
#     return tweets[tweet_id]
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/tweets/{id}", response_class=HTMLResponse)
async def read_tweet(request: Request, id: str):
    tweets = session.query(Tweet).all()
    return templates.TemplateResponse("tweet.html", {"content": tweets[id].content, "id": id})
