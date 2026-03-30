from flask import Flask, render_template, request
from database import init_db, save_meeting, is_slot_available
from email_service import send_confirmation_email
import traceback

app = Flask(__name__)

# Initialize DB
try:
    init_db()
except Exception as e:
    print("DB INIT ERROR:", e)


@app.route('/')
def home():
    return render_template("booking.html")


@app.route('/book', methods=['POST'])
def book():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        if not is_slot_available(date, time):
            return "Slot already booked"

        meet_link = "https://meet.google.com/test-link"

        # Save in DB
        save_meeting(name, email, date, time, meet_link)

        # 🔥 SAFE EMAIL (no crash)
        try:
            send_confirmation_email(email, name, date, time, meet_link)
        except Exception as e:
            print("EMAIL ERROR:", e)

        return f"""
        <h2>SUCCESS ✅</h2>
        <p>Meeting Booked Successfully</p>
        <p>Email sent (if configured correctly)</p>
        """

    except Exception as e:
        return f"<pre>{traceback.format_exc()}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
