import os
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    try:
        print("=== EMAIL FUNCTION STARTED ===")

        url = "https://api.sendgrid.com/v3/mail/send"

        headers = {
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }

        html_content = f"""
        <html>
        <body style="font-family: Arial; background-color:#f4f4f4; padding:20px;">
            <div style="background:white; padding:20px; border-radius:10px;">
                
                <h2 style="color:#6A1B9A;">Akshar Paaul</h2>

                <p>Dear {name},</p>

                <p>Your meeting has been successfully scheduled.</p>

                <p><b>Date:</b> {date}<br>
                <b>Time:</b> {time}</p>

                <p>
                    <a href="{meet_link}" 
                       style="background:#1E73BE; color:white; padding:10px 15px; text-decoration:none; border-radius:5px;">
                       Join Meeting
                    </a>
                </p>

                <p>Thank you.</p>
            </div>
        </body>
        </html>
        """

        data = {
            "personalizations": [
                {
                    "to": [{"email": receiver_email}],
                    "subject": "Meeting Confirmation - Akshar Paaul"
                }
            ],
            "from": {
                "email": "info.aksharpaaul@gmail.com"
            },
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        print("Status Code:", response.status_code)

        if response.status_code == 202:
            print("✅ Email sent successfully")
        else:
            print("❌ Email failed:", response.text)

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
