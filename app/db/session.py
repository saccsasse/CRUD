#the database setup
#sqlalchemy → the ORM (Object Relational Mapper) library to talk to your database.
from sqlalchemy import create_engine #creates the database connection.
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv #allows loading environment variables from a .env file.
import os #to access environment variables.

load_dotenv() #Load .env file

#Each of these reads one variable from the environment.
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

#SQLAlchemy needs a database URL to connect.
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

#The engine manages the connection pool to your DB.
engine = create_engine(DATABASE_URL, echo = True) #echo=True means all SQL statements will be printed in the console
#SessionLocal is a factory that produces new Session objects for each request.
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) #bind=engine → sessions will use the engine we created above.
#autocommit=False → you control when to commit
#autoflush=False → SQLAlchemy won’t automatically push changes to DB until you commit or flush.
Base = declarative_base() #Base is the foundation for all your database models.