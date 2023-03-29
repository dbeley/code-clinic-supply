import os

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL2 = DATABASE_URL.replace("postgres", "postgresql")

Base = declarative_base()
engine = create_engine(
    DATABASE_URL2,
    connect_args={"check_same_thread": False},
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