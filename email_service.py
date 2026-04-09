import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime


def send_confirmation_email(receiver_email, name, date, time, meet_link):

    try:
        # 🔹 Convert date → day
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day = date_obj.strftime("%A")   # Monday, Tuesday...

        message = Mail(
            from_email='info.aksharpaaul@gmail.com',
            to_emails=receiver_email,
            subject='Meeting Confirmation - Akshar Paaul',

            html_content=f"""
            <html>
            <body style="font-family: Arial; background:#f4f6f8; padding:20px;">

                <div style="max-width:600px; margin:auto; background:white; padding:25px; border-radius:10px;">

                    <!-- LOGO -->
                    <div style="text-align:center;">
                        <img src="https://meeting-scheduler-o5wq.onrender.com/static/logo.png" width="90">
                    </div>

                    <h2 style="color:#6A1B9A; text-align:center;">Meeting Confirmed</h2>

                    <p>Dear <b>{name}</b>,</p>

                    <p>Your meeting with <b>Akshar Paaul</b> has been successfully scheduled.</p>

                    <table style="width:100%; margin-top:15px;">
                        <tr>
                            <td><b>Day:</b></td>
                            <td>{day}</td>
                        </tr>
                        <tr>
                            <td><b>Date:</b></td>
                            <td>{date}</td>
                        </tr>
                        <tr>
                            <td><b>Time:</b></td>
                            <td>{time}</td>
                        </tr>
                        <tr>
                            <td><b>Mode:</b></td>
                            <td>Online (Google Meet)</td>
                        </tr>
                    </table>

                    <!-- BUTTON -->
                    <div style="text-align:center; margin:25px;">
                        <a href="{meet_link}"
                           style="background:#1E73BE; color:white; padding:12px 25px;
                                  text-decoration:none; border-radius:6px; font-weight:bold;">
                           Join Meeting
                        </a>
                    </div>

                    <p>Please join the meeting on time.</p>

                    <hr>

                    <p style="font-size:12px; color:gray;">
                        This is an automated email from Akshar Paaul NGO.
                    </p>

                </div>

            </body>
            </html>
            """
        )

        api_key = os.environ.get("SENDGRID_API_KEY")
        sg = SendGridAPIClient(api_key)
        sg.send(message)

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email Error:", e)
