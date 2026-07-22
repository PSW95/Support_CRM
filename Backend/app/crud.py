from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from datetime import datetime
import re

def generate_ticket_id():
    """Generate ticket ID like TKT-001"""
    # In production, you'd want to get the last ID from DB
    import random
    return f"TKT-{random.randint(100, 999)}"

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(
        ticket_id=generate_ticket_id(),
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, status: str = None, search: str = None):
    query = db.query(models.Ticket)
    
    if status and status != "All":
        query = query.filter(models.Ticket.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.ticket_id.ilike(search_term),
                models.Ticket.customer_name.ilike(search_term),
                models.Ticket.customer_email.ilike(search_term),
                models.Ticket.subject.ilike(search_term),
                models.Ticket.description.ilike(search_term)
            )
        )
    
    return query.order_by(models.Ticket.created_at.desc()).all()

def get_ticket(db: Session, ticket_id: str):
    return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()

def update_ticket(db: Session, ticket_id: str, ticket_update: schemas.TicketUpdate):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None
    
    if ticket_update.status:
        db_ticket.status = ticket_update.status
    
    if ticket_update.notes:
        db_note = models.Note(
            ticket_id=db_ticket.id,
            note_text=ticket_update.notes
        )
        db.add(db_note)
    
    db_ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_ticket)
    return db_ticket