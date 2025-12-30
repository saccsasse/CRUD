from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.email import EmailCreate, EmailRead
from app.models.email import Email
from app.tasks.email_tasks import send_email_task
from app.api.deps.deps import get_db

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send", response_model=EmailRead)
def send_email(email: EmailCreate, db: Session = Depends(get_db)):
    """
    Schedule a background email to be sent via Celery
    """
    try:
        email_record = Email(
            recipient=email.recipient,
            subject=email.subject,
            body=email.body,
            sent=False
        )
        db.add(email_record)
        db.commit()
        db.refresh(email_record)

        # Schedule the background task
        send_email_task.delay(email.recipient, email.subject, email.body, email_record.id)
        return email_record

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[EmailRead])
def list_emails(sent: bool | None = None, db: Session = Depends(get_db)):
    """
        List emails from DB. Optional query parameter 'sent' filters by status.
        - sent=true → only sent emails
        - sent=false → only pending emails
        - sent omitted → all emails
    """
    query = db.query(Email)
    if sent is not None:
        query = query.filter(Email.sent == sent)
    emails = query.order_by(Email.timestamp.desc()).all()
    return emails

