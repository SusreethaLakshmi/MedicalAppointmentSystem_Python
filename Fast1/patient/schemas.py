from typing import List,Optional
from pydantic import BaseModel

class Patient(BaseModel):
    patient_name : str
    patient_email : str
    password :str
    class Config():
        orm_mode = True

class ShowPatient(BaseModel):
    patient_id : int
    patient_name : str
    patient_email : str
    password :str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username :str
    password : str

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    patient_email : Optional[str]  = None
    patient_id :int


   
   