from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DB_URL = "sqlite:///.sql_app.db"


#for mysql database use following
#SQLALCHEMY_DB_URL = "mysql://root:root@localhost/first_db"

engine = create_engine(SQLALCHEMY_DB_URL,connect_args={"check_same_thread":False}) #This defines we can use multiple thread and this is for only sqllite
SessionLocal = sessionmaker(autocommit=False,bind=engine)

Base = declarative_base() #This use for the making the models in database