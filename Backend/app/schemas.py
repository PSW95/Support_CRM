from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class TicketBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketCreate(TicketBase):
    pass

class NoteBase(BaseModel):
    note_text: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TicketResponse(BaseModel):
    id: int
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    notes: List[NoteResponse] = []
    
    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class TicketListResponse(BaseModel):
    id: int
    ticket_id: str
    customer_name: str
    subject: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True