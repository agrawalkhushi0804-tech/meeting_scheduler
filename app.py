from flask import Flask, render_template, request
from database import init_db, save_meeting, is_slot_available

app = Flask(__name__)

# Init DB
try:
    init_db()
except Exception as e:
    print("DB ERROR:", e)


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

        save_meeting(name, email, date, time, meet_link)

        return render_template("success.html",
                               name=name,
                               date=date,
                               time=time,
                               meet_link=meet_link)

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
