# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# # check_same_thread...is needed only for SQLite. It's not needed for other databases.
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()




import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/appdb"

SQLALCHEMY_DATABASE_URL = os.getenv("postgresql://postgres:postgres@db:5432/appdb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# # check_same_thread...is needed only for SQLite. It's not needed for other databases.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()

def createSession():
    try:
        Session = SessionLocal()
        return Session
    except Exception as e:
        print("Error al crear la sesión:", str(e))