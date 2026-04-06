import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation_email(receiver_email, name, date, time, meet_link):

    print("Sending email to:", receiver_email)

    try:
        message = Mail(
            from_email='Akshar Paaul <info.aksharpaaul@gmail.com>',  # 🔁 CHANGE THIS
            to_emails=receiver_email,
            subject='Your Meeting Details - Akshar Paaul',
            html_content=f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding:20px;">
                <div style="max-width:600px; margin:auto; background:white; padding:25px; border-radius:10px;">

                    <!-- LOGO -->
                    <div style="text-align:center;">
                        <img src="https://meeting-scheduler-o5wq.onrender.com/static/logo.png"
                             width="100" alt="Akshar Paaul Logo">
                    </div>

                    <h2 style="color:#6A1B9A; text-align:center;">Meeting Confirmation</h2>

                    <p>Dear <b>{name}</b>,</p>

                    <p>Greetings from <b>Akshar Paaul</b>.</p>

                    <p>Your meeting has been successfully scheduled.</p>

                    <p>
                        <b>Date:</b> {date} <br>
                        <b>Time:</b> {time}
                    </p>

                    <div style="text-align:center; margin:20px;">
                        <a href="{meet_link}"
                           style="background:#1E73BE; color:white; padding:12px 20px;
                                  text-decoration:none; border-radius:5px;">
                           Join Meeting
                        </a>
                    </div>

                    <p>Please join on time. We look forward to meeting you.</p>

                    <hr>

                    <p style="font-size:12px; color:gray;">
                        This is an automated email from Akshar Paaul NGO.<br>
                        If you did not request this meeting, please ignore this email.
                    </p>

                </div>
            </body>
            </html>
            """
        )

        # 🔥 Get API key from environment
        api_key = os.environ.get("SENDGRID_API_KEY")

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print("Email sent successfully")
        print("Status Code:", response.status_code)

    except Exception as e:
        print("SendGrid Error:", e)
