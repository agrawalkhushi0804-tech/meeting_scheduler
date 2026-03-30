import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    try:
        # Get API key from environment variable
        api_key = os.getenv("SENDGRID_API_KEY")

        if not api_key:
            print("❌ SENDGRID_API_KEY not found")
            return

        sg = SendGridAPIClient(api_key)

        subject = "Meeting Scheduled - Akshar Paaul"

        html_content = f"""
        <div style="font-family: Arial; max-width:600px; margin:auto; padding:20px;">
            
            <h2 style="color:#1E73BE;">अक्षर पाऊल</h2>
            <p style="color:#555;">संस्कारातून साक्षरतेकडे…</p>

            <hr>

            <p>Dear {name},</p>

            <p>Your meeting has been successfully scheduled.</p>

            <p>
                <b>Date:</b> {date}<br>
                <b>Time:</b> {time}
            </p>

            <p>Click below to join your meeting:</p>

            <a href="{meet_link}" 
               style="background:#1E73BE; color:white; padding:10px 15px; text-decoration:none; border-radius:5px;">
               Join Meeting
            </a>

            <br><br>

            <p style="font-size:13px; color:gray;">
                Regards,<br>
                Akshar Paaul Team
            </p>

        </div>
        """

        message = Mail(
            from_email='Akshar Paaul <agrawalkhushi0804@gmail.com>',  # must be verified in SendGrid
            to_emails=receiver_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=f"""
Meeting Scheduled

Date: {date}
Time: {time}

Join here: {meet_link}
"""
        )

        response = sg.send(message)

        print("✅ Email sent successfully")
        print("Status Code:", response.status_code)

    except Exception as e:
        print("❌ SendGrid Error:", e)
