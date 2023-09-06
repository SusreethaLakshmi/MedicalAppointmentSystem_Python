from sqlalchemy import Column,Integer,String
from database import Base
from sqlalchemy.orm import relationship

class Doctor(Base):
    __tablename__ = 'doctors'

    doc_id = Column(Integer,primary_key = True,index = True)
    doc_name = Column(String(255))
    doc_specification = Column(String(255))
    doc_email = Column(String(255),unique=True)
    doc_degree = Column(String(255))
    password = Column(String(255))
   
