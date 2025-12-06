from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint, constr

class EventSubmission(BaseModel):
    eventName: constr(min_length=3, max_length=30)
    eventDesc: constr(max_length=500)
    eventLocation: constr(max_length=500)
    eventDatetime: datetime
        
# record classes add datetime
class EventSubmissionRecord(EventSubmission):
    receivedAt: datetime
    eventHash: str
    eventId: constr(min_length=6, max_length=6)

class CarSubmission(BaseModel):
    driverName: constr(min_length=3, max_length=30)
    numberSeats: conint(gt=0, le=15)
    takenSeats: int

class RiderSubmission(BaseModel):
    riderName: constr(min_length=3, max_length=30)
    riderPhone: conint(ge=1000000000, le=9999999999)