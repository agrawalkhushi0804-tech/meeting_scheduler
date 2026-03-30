from flask import Flask, render_template, request
from database import init_db, save_meeting, is_slot_available
from email_service import send_confirmation_email
import threading

app = Flask(__name__)

# Init DB
try:
    init_db()
except Exception as e:
    print("DB ERROR:", e)


@app.route('/')
def home():
    return render_template("booking.html")


# 🔥 BACKGROUND EMAIL FUNCTION
def send_email_background(email, name, date, time, meet_link):
    try:
        send_confirmation_email(email, name, date, time, meet_link)
    except Exception as e:
        print("EMAIL ERROR:", e)


@app.route('/book', methods=['POST'])
def book():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        if not is_slot_available(date, time):
            return "Slot already booked"

        meet_link = "https://meet.google.com/your-real-link"

        save_meeting(name, email, date, time, meet_link)

        # 🔥 SEND EMAIL IN BACKGROUND (NO CRASH)
        threading.Thread(
            target=send_email_background,
            args=(email, name, date, time, meet_link)
        ).start()

        return render_template("success.html",
                               name=name,
                               date=date,
                               time=time,
                               meet_link=meet_link)

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)


