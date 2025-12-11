from src.services.db.db_manager import Database 
from datetime import datetime
import  src.services.senders.send_emails as senders

CONTACT_PAGE = Database(table="candidate_data.contact")

def submit_request(contact):
    ##before sending or after,send email to our email: with request with unread
    currrent_date = datetime.now()
    
    query = """
    INSERT INTO candidate_data.contact(name,lastName,email,asunto,mensaje,createdat)
    VALUES(%s,%s,%s,%s,%s,%s)
    """
    conn = CONTACT_PAGE._get_conn()

    try:
        with conn.cursor() as cur:
                cur.execute(query,(contact.get("name"),contact.get("lastName"),contact.get("email"),contact.get("asunto"),contact.get("mensaje"),currrent_date))
                conn.commit()
    finally:
            CONTACT_PAGE._release_conn(conn)
    
    senders.send_email_to_client(contact.get("email"),contact.get("name"))
    senders.send_update_email_to_admins()