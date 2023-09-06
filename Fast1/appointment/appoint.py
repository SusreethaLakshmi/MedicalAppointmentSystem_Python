import select
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import models,schemas

def createbookings(request: schemas.ShowBooking,db :Session):
    bookingss = models.Booking(patname = request.patname,patage = request.patage , patproblem = request.patproblem,MobileNo =request.MobileNo,wday=request.wday,sid =request.sid,pid = request.pid,did = request.did)
    db.add(bookingss)
    db.commit()
    db.refresh(bookingss)
    db.close()
    return bookingss

def get_all(db:Session):
    bookingss = db.query(models.Booking).all()
    return bookingss

def get_booking_id (id : int,db:Session):
    bookingss =db.query(models.Booking).filter(models.Booking.bid== id).first()
    return bookingss

def get_booking_doc (id : int,db:Session ):
    doc =db.query(models.Booking).filter(models.Booking.did== id).all()
    return doc

def update_booking(id:int,request:schemas.Booking, db:Session):
    booking = db.query(models.Booking).filter(models.Booking.bid == id).update(request.dict())
    db.commit()
    db.close()
    return request.dict()


def update_slot_after_booking(sid:int,did:int,wday:str,db:Session):
    slots = db.query(models.Slot).filter(models.Slot.slots == sid,models.Slot.did==did,models.Slot.days==wday).update({models.Slot.isbook:"1"},synchronize_session = False)
    db.commit()
    db.close()

def update_slot_after_editing(sid:int,db:Session):
    slots = db.query(models.Slot).filter(models.Slot.sid == sid).update({models.Slot.isbook:"0"},synchronize_session = False)
    db.commit()
    db.close()

def update_slot(id:int,request:schemas.ShowSlot, db:Session):
    slots = db.query(models.Slot).filter(models.Slot.slots == id).update(request.dict())
    db.commit()
    db.close()
    return request.dict()

def get_booking_pid (id : int,db:Session):
    pat =db.query(models.Booking).filter(models.Booking.pid == id).all()
    return pat

def get_booking_allpatients (id : int,db:Session):
    pat =db.query(models.Booking).filter(models.Booking.pid== id).all()
    return pat

def slotcreate(request: schemas.Slot,db :Session ):
    slot = models.Slot(sid = request.sid,did = request.did,days= request.days,slots = request.slots)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    db.close()
    return slot

def deleteAppointment(id:int,db:Session):
    delbook = db.query(models.Booking).filter(models.Booking.bid==id).one()
    db.delete(delbook)
    db.commit()
    db.close()
    return delbook

def get_slot_all(db:Session ):
    slots = db.query(models.Slot).all()
    return slots

def get_slots_id(id: int,db:Session):
    slot =db.query(models.Slot).filter(models.Slot.sid==id).first()
    return slot

def get_slot_doc (id : int,db:Session ):
    slots =db.query(models.Slot).filter(models.Slot.did== id).all()
    return slots

def get_slot_day (id : int,days :str ,db:Session ):
    slots =db.query(models.Slot).where(models.Slot.did== id,models.Slot.days==days).all()
    return slots

def get_slot_daySlot(id : int,days :str,slots:int ,db:Session ):
    slot =db.query(models.Slot).where(models.Slot.did== id,models.Slot.days==days,models.Slot.slots == slots).all()
    return slot






    




