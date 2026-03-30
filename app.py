from flask import Flask, render_template, request
from database import init_db, save_meeting, is_slot_available
import traceback

app = Flask(__name__)

# Init DB
try:
    init_db()
    print("DB OK")
except Exception as e:
    print("DB ERROR:", e)


@app.route('/')
def home():
    return render_template("booking.html")


@app.route('/book', methods=['POST'])
def book():
    try:
        print("STEP 1")

        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        print("STEP 2", name, email)

        if not is_slot_available(date, time):
            return "Slot already booked"

        print("STEP 3")

        meet_link = "https://meet.google.com/test-link"

        print("STEP 4")

        save_meeting(name, email, date, time, meet_link)

        print("STEP 5 SAVED")

        return "SUCCESS DATABASE WORKING"

    except Exception as e:
        return f"<pre>{traceback.format_exc()}</pre>"


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
