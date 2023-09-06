from typing import List,Optional
from pydantic import BaseModel
from datetime import date

class Booking(BaseModel):
    patname : str
    patage : int
    patproblem : str
    MobileNo : str
    did : int
    wday : str
    sid :int
    pid : int
    class Config():
        orm_mode = True

class ShowBooking(BaseModel):
    bid:int
    patname : str
    patage : int
    patproblem : str
    MobileNo : str
    did : int
    wday : str
    pid :int
    sid : int
    class Config():
        orm_mode = True

class Slot(BaseModel):
    sid : int
    did : int
    days : str
    slots : int
    isbook : int
    class Config():
        orm_mode = True

class ShowSlot(BaseModel):
    did : int
    days : str
    slots : int
    isbook : int
    class Config():
        orm_mode = True


