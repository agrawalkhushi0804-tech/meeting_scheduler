import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation_email(receiver_email, name, date, time, meet_link):
    try:
        api_key = os.getenv("SENDGRID_API_KEY")

        if not api_key:
            print("❌ SENDGRID_API_KEY not found")
            return

        sg = SendGridAPIClient(api_key)

        subject = "Your Meeting Details - Akshar Paaul"

        html_content = f"""
        <div style="font-family: Arial; max-width:600px; margin:auto; padding:20px;">
            
            <div style="text-align:center;">
                <img src="https://i.postimg.cc/YOUR-LINK/logo.png" width="100" alt="Akshar Paaul Logo">
                <h2 style="color:#1E73BE;">अक्षर पाऊल</h2>
                <p style="color:#555;">संस्कारातून साक्षरतेकडे…</p>
            </div>

            <hr>

            <p>Dear {name},</p>

            <p>Your meeting has been successfully scheduled.</p>

            <p>
                <b>Date:</b> {date}<br>
                <b>Time:</b> {time}
            </p>

            <p>You can join your meeting using the link below:</p>

            <p>
                <a href="{meet_link}">{meet_link}</a>
            </p>

            <br>

            <hr>
            <p style="font-size:12px; color:gray;">
                This is an automated email sent by Akshar Paaul NGO.<br>
                If you did not request this meeting, you can safely ignore this email.
            </p>

        </div>
        """

        message = Mail(
            from_email='agrawalkhushi0804@gmail.com',  # cleaner sender
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
