from sqlalchemy import Column,Integer,String
from database import Base
from sqlalchemy.orm import relationship

class Booking(Base):
    __tablename__ = "bookings"

    bid = Column(Integer,primary_key = True,index = True)
    patname = Column(String(255))
    patage = Column(Integer)
    patproblem = Column(String(255))
    MobileNo = Column(String(255))
    did = Column(Integer)
    wday = Column(String(255))
    pid = Column(Integer)
    sid = Column(Integer)

class Slot(Base):
    __tablename__ ="slots"

    sid = Column(Integer,primary_key = True,index = True)
    did = Column(Integer)
    days = Column(String(255))
    slots = Column(Integer)
    isbook = Column (Integer)

    
   
