from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator, conint, constr

class EventSubmission(BaseModel):
    eventName: str = Field(..., min_length=3, max_length=30)
    eventDesc: str = Field(..., max_length=500)
        
# record classes add datetime
class EventSubmissionRecord(EventSubmission):
    receivedAt: datetime
    eventHash: str
    eventId: str = Field(..., min_length=6, max_length=6)

class CarSubmission(BaseModel):
    driverName: str = Field(..., min_length=3, max_length=30)
    numberSeats: conint(le=15)
    takenSeats: int

class RiderSubmission(BaseModel):
    riderName = constr(min_length=3, max_length=30)