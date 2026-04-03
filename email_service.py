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

        subject = "Meeting Scheduled - Akshar Paaul"

        html_content = f"""
        <div style="font-family: Arial; max-width:600px; margin:auto; padding:20px; text-align:center;">
            
            <!-- 🔥 LOGO -->
           <img src="https://i.postimg.cc/cJbv2bTY/logo.png" 
                 alt="Akshar Paaul Logo" 
                 width="100" 
                 style="display:block; margin:auto;">
            <h2 style="color:#1E73BE; margin:5px;">अक्षर पाऊल</h2>
            <p style="color:#555;">संस्कारातून साक्षरतेकडे…</p>

            <hr>

            <div style="text-align:left;">

            <p>Dear {name},</p>

            <p>Your meeting has been successfully scheduled.</p>

            <p>
                <b>Date:</b> {date}<br>
                <b>Time:</b> {time}
            </p>

            <p>Click below to join your meeting:</p>

            <div style="text-align:center; margin:20px 0;">
                <a href="{meet_link}" 
                   style="background:#1E73BE; color:white; padding:12px 20px; text-decoration:none; border-radius:6px; font-weight:bold;">
                   Join Meeting
                </a>
            </div>

            <p style="font-size:13px; color:gray;">
                Regards,<br>
                Akshar Paaul Team
            </p>

            </div>

        </div>
        """

        message = Mail(
            from_email='agrawalkhushi0804@gmail.com',
            to_emails=receiver_email,
            subject="Your Meeting Details - Akshar Paaul",
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
<hr>
<p style="font-size:12px; color:gray;">
This is an automated email sent by Akshar Paaul NGO.<br>
If you did not request this meeting, you can safely ignore this email.
</p>
