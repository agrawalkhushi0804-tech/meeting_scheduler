import smtplib
import ssl
import os
from email.message import EmailMessage


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    try:
        SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        APP_PASSWORD = os.getenv("APP_PASSWORD")

        if not SENDER_EMAIL or not APP_PASSWORD:
            print("Email credentials missing")
            return

        subject = "Meeting Confirmation | Akshar Paaul"

        html_content = f"""
        <html>
        <body>
            <h2>Meeting Confirmed</h2>
            <p>Hello {name},</p>
            <p>Your meeting is scheduled.</p>
            <p><b>Date:</b> {date}</p>
            <p><b>Time:</b> {time}</p>
            <p><a href="{meet_link}">Join Meeting</a></p>
        </body>
        </html>
        """

        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content("Your email client does not support HTML")
        msg.add_alternative(html_content, subtype="html")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print("EMAIL FAILED:", e)
