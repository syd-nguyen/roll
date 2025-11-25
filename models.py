from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

class EventSubmission(BaseModel):
    eventName: str = Field(..., min_length=3, max_length=30)
    #eventDesc: str = Field(..., max_length=500)
        
# record classes add datetime
class EventSubmissionRecord(EventSubmission):
    received_at: datetime