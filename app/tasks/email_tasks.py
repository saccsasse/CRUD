from mailslurp_client import Configuration, ApiClient, SendEmailOptions, InboxControllerApi

from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.email import Email

MAILSLURP_API_KEY = "bf003ba4306bc3f62a6095e53dc128d40dfa041d06ced38f107ef87a5a7cfa1f"

@celery_app.task(name="send_email_task")
def send_email_task(recipient: str, subject: str, body: str, email_id: int):
    """
        Automatically create a temporary MailSlurp inbox and send an email via Celery.
    """
    db: Session = SessionLocal()
    try:
        # Load the pending email record
        email_record = db.query(Email).get(email_id)

        configuration = Configuration()
        configuration.api_key['x-api-key'] = MAILSLURP_API_KEY

        with ApiClient(configuration) as api_client:
            inbox_controller = InboxControllerApi(api_client)

            # Create temporary inbox
            inbox = inbox_controller.create_inbox()
            inbox_id = inbox.id

            send_options = SendEmailOptions(
                to=[recipient],
                subject=subject,
                body=body
            )
            inbox_controller.send_email(inbox_id, send_options)

        #Update email as sent
        email_record.sent = True
        db.commit()
        print(f"Email sent to {recipient} via MailSlurp")
        return {"status": "success", "email_id": email_record.id}

    except Exception as e:
        print(f"Error sending email: {e}")
        raise e

    finally:
        db.close()