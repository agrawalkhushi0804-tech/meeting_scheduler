import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

        message = Mail(
            from_email='agrawalkhushi0804@gmail.com',
            to_emails=receiver_email,
            subject='Meeting Confirmation | Akshar Paaul',
            html_content=f"""
            <h2>Meeting Confirmed</h2>
            <p>Hello {name},</p>
            <p>Your meeting is scheduled.</p>
            <p><b>Date:</b> {date}</p>
            <p><b>Time:</b> {time}</p>
            <p><a href="{meet_link}">Join Meeting</a></p>
            """
        )

        sg.send(message)
        print("Email sent successfully")

    except Exception as e:
        print("SendGrid Error:", e)
