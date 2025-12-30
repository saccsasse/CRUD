#the database setup
#sqlalchemy → the ORM (Object Relational Mapper) library to talk to your database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os


load_dotenv()


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")


DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


engine = create_engine(DATABASE_URL, echo = True) #echo=True means all SQL statements will be printed in the console
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) #bind=engine → sessions will use the engine created above
#autoflush=False → SQLAlchemy won’t automatically push changes to DB until you commit or flush.
Base = declarative_base()