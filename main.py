from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine(
    "sqlite:///example.db",
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