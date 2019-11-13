from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///db/main.db", echo=True)

Base = declarative_base()
Session = sessionmaker()

engine.metadate.create_all(Base)