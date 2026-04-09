import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation_email(receiver_email, name, date, time, meet_link):

    print("=== EMAIL FUNCTION STARTED ===")
    print("Receiver:", receiver_email)

    try:
        api_key = os.environ.get("SENDGRID_API_KEY")

        print("API KEY FOUND:", api_key is not None)

        if not api_key:
            print("❌ ERROR: API key missing")
            return

        message = Mail(
            from_email='infoaksharpaaul@gmail.com',  # 👈 CHANGE THIS
            to_emails=receiver_email,
            subject='Meeting Confirmation - Akshar Paaul',
            html_content=f"""
            <h2>Meeting Confirmed</h2>
            <p>Hello {name},</p>
            <p>Your meeting is scheduled.</p>
            <p><b>Date:</b> {date}</p>
            <p><b>Time:</b> {time}</p>
            <a href="{meet_link}">Join Meeting</a>
            """
        )

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print("✅ EMAIL SENT")
        print("Status Code:", response.status_code)

    except Exception as e:
        print("❌ ERROR SENDING EMAIL:", str(e))
