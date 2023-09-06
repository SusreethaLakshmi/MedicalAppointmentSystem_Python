from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL ='mysql://root:Susreetha123@127.0.0.1:3306/patientdb'

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False,)

Base =  declarative_base()



