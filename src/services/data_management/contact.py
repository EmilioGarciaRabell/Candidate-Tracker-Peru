from src.services.db.db_manager import Database 
import  src.services.senders.send_emails as senders
from datetime import datetime, timezone

CONTACT_PAGE = Database(table="candidate_data.contact")


def submit_request(contact: dict) -> None:
    current_date = datetime.now(timezone.utc)

    insert_sql = """
        INSERT INTO candidate_data.contact
            (name, lastname, email, asunto, mensaje, createdat)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    CONTACT_PAGE.execute(
        insert_sql,
        (
            contact.get("name"),
            contact.get("lastName"),
            contact.get("email"),
            contact.get("asunto"),
            contact.get("mensaje"),
            current_date,
        ),
    )

    # after DB insert succeeds → notify
    senders.send_email_to_client(contact.get("email"), contact.get("name"))
    senders.send_update_email_to_admins()
