""" import databases
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base


# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:diatta96@localhost/projet_sgbd"

db = databases.Database(DATABASE_URL)

Base = declarative_base()

engine = create_engine(DATABASE_URL) """
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:diatta96@localhost/projet_sgbd"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()