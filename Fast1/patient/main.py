from fastapi import FastAPI,Depends,status,APIRouter,HTTPException
import models,schemas,oauth
from hashing import Hash
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import Token as Token
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:4200",
    "https://localhost:8000",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/patient',response_model=schemas.Patient,tags=['To Create Patients details'],status_code = status.HTTP_201_CREATED)
def create(request: schemas.Patient,db :Session  = Depends(get_db)):
    new_patient = models.Patient(patient_name = request.patient_name,patient_email = request.patient_email,password = Hash.bcrypt(request.password))
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    db.close()
    return new_patient

@app.get('/patient',response_model=List[schemas.ShowPatient],tags=[' View Patients'])
def get_all_patient(db:Session  = Depends(get_db)):
    patient = db.query(models.Patient).all()
    return patient

@app.get('/patient/{id}',response_model=list[schemas.Patient])
def get_patient(id : int,db:Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == id).all()
    return patient

@app.get('/patient/{name}',response_model=list[schemas.ShowPatient])
def get_patient_name(name:str,db:Session = Depends(get_db)):
    patients = db.query(models.Patient).filter(models.Patient.patient_name == name).first()
    return patients

@app.get('/patient/{email}',response_model=list[schemas.Patient])
def get_patient_email(email:str,db:Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_email == email).all()
    return patient

@app.delete('/patient',status_code = status.HTTP_204_NO_CONTENT,tags=['To Remove patients'])
def delete(id,db:Session  = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.patient_id == id).delete(synchronize_session = False)
    db.commit()
    return 'Done'

@app.put('/patient',status_code = status.HTTP_202_ACCEPTED,tags=['To Update patients'])
def update(id,request: schemas.Patient,db:Session  = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.patient_id == id).update(request.dict())
    new_patient = models.Patient(patient_name = request.patient_name,patient_email = request.patient_email,password = Hash.bcrypt(request.password))
    db.commit()
    return new_patient

@app.post('/login',tags = ["Authentication"])
def login(request:schemas.Login,db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_email == request.username).first()
    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Invalid Credentials")

    
    access_token =  Token.create_access_token(data={"subid":patient.patient_id})
    current_user = oauth.get_current_user(access_token)
    return { "access_token":access_token, "user":current_user}
        
    



