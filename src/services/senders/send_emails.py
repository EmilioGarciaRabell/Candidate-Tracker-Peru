import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from psycopg2.extras import RealDictCursor
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

load_dotenv()

EMAIL_ID = os.environ.get("EMAIL_ID")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def send_email_to_client(email, name):
    # Crear el mensaje
    msg = MIMEMultipart("alternative")
    msg["From"] = f"informate.pe <{EMAIL_ID}>"
    msg["To"] = email
    msg["Subject"] = "Hemos recibido tu mensaje – informate.pe"

    # Contenido HTML bonito
    html = f"""
        <html>
        <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f6f8;">
            <table width="100%" cellpadding="0" cellspacing="0" style="padding: 20px 0;">
                <tr>
                    <td align="center">
                        <table width="100%" style="max-width:600px; background:#ffffff; border-radius:12px; padding:30px;">
                            
                            <tr>
                                <td style="text-align:center;">
                                    <h1 style="color:#2d3748; margin:0;">informate.pe</h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 20px 0;">
                                    <h2 style="color:#1a202c;">¡Hola {name}!</h2>
                                    <p style="font-size:16px; color:#4a5568; line-height:1.6;">
                                        Gracias por contactar con <strong>informate.pe</strong>.  
                                        Hemos recibido tu mensaje correctamente y nuestro equipo lo revisará lo antes posible.
                                    </p>
                                    <p style="font-size:16px; color:#4a5568; line-height:1.6;">
                                        Si tu consulta es urgente, por favor responde a este correo y te atenderemos prioritariamente.
                                    </p>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding-top: 20px; border-top:1px solid #e2e8f0;">
                                    <p style="font-size:14px; color:#718096;">
                                        Atentamente,<br>
                                        <strong>Equipo de informate.pe</strong>
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
    """


    # Adjuntar versiones texto + HTML
    text = f"""Hola {name},

        Gracias por contactar con informate.pe.
        Hemos recibido tu mensaje y te responderemos pronto.

        Atentamente,
        Equipo informate.pe
    """

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

   

    with smtplib.SMTP(host="mail.privateemail.com", port=587, timeout=10) as smtp_obj:
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.ehlo()
        smtp_obj.login(EMAIL_ID, EMAIL_PASSWORD)
        smtp_obj.sendmail(EMAIL_ID, email, msg.as_string())

def get_unread():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT id, name, email, mensaje, status, createdat
            FROM candidate_data.contact
            WHERE status = 'unread'
        """
        cur.execute(query)

        data = cur.fetchall()  
        return data

    except Exception as e:
        print("Error:", e)
        if conn:
            conn.rollback()
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_admins():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT id, name, email
            FROM candidate_data.admins
        """
        cur.execute(query)

        data = cur.fetchall()   
        return data

    except Exception as e:
        print("Error:", e)
        if conn:
            conn.rollback()
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def send_update_email_to_admins():


    unread = get_unread()
    admins = get_admins()

    if not unread or not admins:
        return

    # Build HTML body
    html_rows = ""
    for msg in unread:
        html_rows += f"""
        <tr>
            <td style="padding:8px; border:1px solid #ddd;">{msg['id']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{msg['name']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{msg['email']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{msg['mensaje']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{msg['createdat']}</td>
        </tr>
        """

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 20px;">
        <div style="max-width: 700px; margin: auto; background: #ffffff; padding: 20px; border-radius: 8px;">
          <h2 style="color: #333;">Unread Contact Messages</h2>
          <p style="color: #555;">
            You have the following unread messages:
          </p>

          <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
              <tr style="background-color: #f1f1f1;">
                <th style="padding:8px; border:1px solid #ddd;">ID</th>
                <th style="padding:8px; border:1px solid #ddd;">Name</th>
                <th style="padding:8px; border:1px solid #ddd;">Email</th>
                <th style="padding:8px; border:1px solid #ddd;">Message</th>
                <th style="padding:8px; border:1px solid #ddd;">Date</th>
              </tr>
            </thead>
            <tbody>
              {html_rows}
            </tbody>
          </table>

          <p style="color:#777; margin-top:20px; font-size:12px;">
            This is an automated notification.
          </p>
        </div>
      </body>
    </html>
    """

    # Send email to each admin
    for admin in admins:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"informate.pe <{EMAIL_ID}>"
        msg["To"] = admin["email"]
        msg["Subject"] = "Unread Contact Messages – Action Required"

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP("mail.tudominio.com", 587) as s:
            s.starttls()
            s.login(EMAIL_ID, EMAIL_PASSWORD)
            s.sendmail(EMAIL_ID, admin["email"], msg.as_string())

