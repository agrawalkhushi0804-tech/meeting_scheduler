import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# Load .env file
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    subject = "Meeting Confirmation | [Akshar Paaul]"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px;">
            
            <h2 style="color: #2E86C1;">Meeting Confirmation</h2>
            
            <p>Dear <strong>{name}</strong>,</p>
            
            <p>Greetings from <strong>Akshar Paaul</strong>.</p>
            
            <p>Your meeting has been successfully scheduled. Please find the details below:</p>

            <table style="width:100%; margin-top:15px; margin-bottom:15px;">
                <tr>
                    <td><strong>Date:</strong></td>
                    <td>{date}</td>
                </tr>
                <tr>
                    <td><strong>Time:</strong></td>
                    <td>{time}</td>
                </tr>
                <tr>
                    <td><strong>Mode:</strong></td>
                    <td>Online (Google Meet)</td>
                </tr>
            </table>

            <div style="text-align:center; margin: 25px 0;">
                <a href="{meet_link}" 
                   style="background-color:#2E86C1; color:white; padding:12px 25px; 
                   text-decoration:none; border-radius:5px; font-weight:bold;">
                   Join Meeting
                </a>
            </div>

            <p>Please ensure you join the meeting on time.</p>

            <hr style="margin-top:30px;">

            <p style="font-size:14px; color:gray;">
                Warm regards,<br>
                <strong>Akshar Paaul</strong><br>
                📧 aksharpaaul@gmail.com<br>
                📞 +91 8856935553
            </p>

        </div>
    </body>
    </html>
    """

    try:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.set_content("Your email client does not support HTML.")
        msg.add_alternative(html_content, subtype="html")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print("Error sending email:", e)