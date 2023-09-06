from fastapi import FastAPI,Depends,status,APIRouter,HTTPException
import models,schemas,oauth
from sqlalchemy import Column,Integer,String
from hashing import Hash
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import Token as Token
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "https://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/doctor',response_model=schemas.Doctor,tags=[' Create Doctor details'],status_code = status.HTTP_201_CREATED)
def create(request: schemas.Doctor,db :Session  = Depends(get_db)):
    new_doctor = models.Doctor(doc_name = request.doc_name,doc_specification = request.doc_specification,doc_email =request.doc_email ,doc_degree=request.doc_degree, password = Hash.bcrypt(request.password))
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@app.get('/doctor',response_model=List[schemas.ShowDoctor],tags=[' View Doctors'])
def show(db:Session  = Depends(get_db)):
    doctors = db.query(models.Doctor).all()
    return doctors

@app.get('/doctor/{id}',response_model=schemas.ShowDoctor,tags=['Doctor'])
def get_doctor(id,db:Session  = Depends(get_db)):
    doctors = db.query(models.Doctor).filter(models.Doctor.doc_id == id).first()
    return doctors

@app.delete('/doctor',status_code = status.HTTP_204_NO_CONTENT,tags=['Remove doctors'])
def delete(id,db:Session  = Depends(get_db)):
    db.query(models.Doctor).filter(models.Doctor.doc_id == id).delete(synchronize_session = False)
    db.commit()
    return 'Done'

@app.put('/doctor',status_code = status.HTTP_202_ACCEPTED,tags=['Update doctors'])
def update(id,request: schemas.ShowDoctor,db:Session  = Depends(get_db)):
    db.query(models.Doctor).filter(models.Doctor.doc_id == id).update(request.dict())
    new_doctor = models.Doctor(doc_name = request.doc_name,doc_specification = request.doc_specification,doc_email = request.doc_email,password = Hash.bcrypt(request.password))   
    db.commit()
    return new_doctor

@app.post('/login',tags = ["Authentication"])
def login(request:schemas.Login,db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doc_email == request.username).first()
    if not doctor:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Invalid Credentials")
    
    access_token =  Token.create_access_token(data={"subid": doctor.doc_id})
    current_user = oauth.get_current_user(access_token)
    return { "doc_access_token":access_token, "user":current_user}
        
    



