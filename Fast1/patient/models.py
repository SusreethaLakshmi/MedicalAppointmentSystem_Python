from sqlalchemy import Column,Integer,String
from database import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(Integer,primary_key = True,index = True)
    patient_name = Column(String(255))
    patient_email = Column(String(255),unique = True)
    password = Column(String(255))
   
