from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, save_meeting, get_all_meetings, is_slot_available, clear_all_meetings
from calendar_service import get_calendar_service, create_google_meet
from email_service import send_confirmation_email
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

init_db()

# =========================
# HOME
# =========================
@app.route('/')
def home():
    return render_template("booking.html")


# =========================
# BOOK MEETING
# =========================
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    if not is_slot_available(date, time):
        return "Slot already booked!"

    service = get_calendar_service()
    meet_link = create_google_meet(service, name, date, time)

    save_meeting(name, email, date, time, meet_link)

    try:
        send_confirmation_email(email, name, date, time, meet_link)
    except Exception as e:
        print("Email Error:", e)

    return render_template("success.html",
                           name=name,
                           date=date,
                           time=time,
                           meet_link=meet_link)


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == os.getenv("ADMIN_USERNAME", "admin") and password == os.getenv("ADMIN_PASSWORD", "admin123"):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials"

    return render_template("login.html")


# =========================
# ADMIN DASHBOARD
# =========================
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    meetings = get_all_meetings()
    return render_template("admin.html", meetings=meetings)


# =========================
# 🔥 CLEAR ALL MEETINGS
# =========================
@app.route('/clear')
def clear():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    clear_all_meetings()
    return "✅ All meetings cleared successfully!"


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)




