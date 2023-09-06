from typing import List,Optional
from pydantic import BaseModel

class Doctor(BaseModel):
    doc_name : str
    doc_specification : str
    doc_email : str
    doc_degree:str
    password :str
    class Config():
        orm_mode = True

class ShowDoctor(BaseModel):
    doc_id : int
    doc_name : str
    doc_specification : str
    doc_email : str
    doc_degree:str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username :str
    password : str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    doc_email : Optional[str] = None
    doc_id :int


   
   