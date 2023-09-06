from fastapi import FastAPI,Depends,status,APIRouter,HTTPException
import models,schemas,appoint
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(engine)
app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/booking',response_model=list[schemas.ShowBooking])
def display_all_bookings(db:Session = Depends(get_db)):
    return appoint.get_all(db)

@app.get('/bookingss/{id}',response_model = schemas.ShowBooking)
def display_booking(id:int,db:Session = Depends(get_db)):
    bookingss = appoint.get_booking_id(id,db)
    if not bookingss:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Appointment with this ID doesnot exist")
    else:
        return bookingss

@app.post('/booking')
def createbookings(request:schemas.Booking,db:Session=Depends(get_db)):
    # if appoint.get_booking_id(request.bid,db):
    #     raise HTTPException(status_code = status.HTTP_208_ALREADY_REPORTED,detail = "User already exists")
    # else:
        bookingss = appoint.createbookings(request,db)
        appoint.update_slot_after_booking(bookingss.sid,bookingss.did,bookingss.wday,db)
        return bookingss
   
#,response_model=list[schemas.ShowBooking]
@app.get('/booking/{id}')
def get_booking_doctorId (id : int,db:Session = Depends(get_db)):
    docapps = appoint.get_booking_doc(id,db)
    return docapps

@app.put('/booking/{bid}')
def updatebooking(bid:int,request:schemas.Booking,db:Session=Depends(get_db)):
    booking = appoint.update_booking(bid,request,db)
    appoint.update_slot_after_booking(booking['sid'],booking['did'],booking['wday'],db)
    return booking

@app.get('/patbooking/{id}')
def get_booking_allpatients(id:int,db:Session = Depends(get_db)):
    patall = appoint.get_booking_allpatients(id,db)
    return patall

@app.get('/patientbooking/{id}',response_model=list[schemas.ShowBooking])
def get_booking_pid (id : int,db:Session = Depends(get_db)):
    pat = appoint.get_booking_pid(id,db)
    return pat

@app.delete('/booking/{bid}') 
def delete(bid:int,db:Session  = Depends(get_db)):
    delbook = appoint.get_booking_id(bid,db)
    appoint.update_slot_after_booking(delbook.sid,delbook.did,delbook.wday,db)
    delbook1 = appoint.deleteAppointment(bid,db)

@app.post('/slot')
def create_slot(request:schemas.Slot,db:Session=Depends(get_db)):
    if appoint.get_slots_id(request.sid,db):
        raise HTTPException(status_code = status.HTTP_208_ALREADY_REPORTED,detail = "Slot already exists")
    else:
        slot = appoint.slotcreate(request,db)
        return slot
    
@app.get('/slot',response_model=list[schemas.Slot])
def getslots(db:Session = Depends(get_db)):
    return appoint.get_slot_all(db)


@app.get('/slot/{id}',response_model=list[schemas.Slot])
def docslot(id:int,db:Session=Depends(get_db)):
    slot = appoint.get_slot_doc(id,db)
    return slot

@app.get('/slot/{id}/{day}',response_model=list[schemas.Slot])
def docdayslot(id:int,day:str,db:Session=Depends(get_db)):
    slot = appoint.get_slot_day(id,day,db)
    return slot

@app.get('/slot/{id}/{day}/{slots}',response_model=list[schemas.Slot])
def docdayslot(id:int,day:str,slots:int,db:Session=Depends(get_db)):
    slot = appoint.get_slot_daySlot(id,day,slots,db)
    return slot

@app.put('/slot',status_code = status.HTTP_202_ACCEPTED,tags=['To Update Slots'])
def update(id,request: schemas.Slot,db:Session  = Depends(get_db)):
    db.query(models.Slot).filter(models.Slot.sid == id).update(request.dict())
    new_slot = models.Slot(did = request.did,days = request.days, slots = request.slots,isbook = request.isbook)
    db.commit()
    return new_slot

@app.put('/slots/{sid}')
def updateslot(id:int,request:schemas.ShowSlot,db:Session= Depends(get_db)):
    slot = appoint.update_slot(id,request,db)
    return slot

@app.put('/slotafterbooking/{id}')
def updateslot(id:int,request:schemas.ShowSlot,db:Session= Depends(get_db)):
    slot = appoint.update_slot_after_editing(id,db)
    return slot

@app.delete('/slot/{sid}/{did}/{date}',status_code = status.HTTP_204_NO_CONTENT,tags=['To Remove Slots'])
def delete(sid:int,did:int,wday:str,db:Session  = Depends(get_db)):
    db.query(models.Slot).filter(models.Slot.slots == sid,models.Slot.did==did,models.Slot.days==wday).delete(synchronize_session = False)
    db.commit()
    return 'Done'





