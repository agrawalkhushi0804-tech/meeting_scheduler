from flask import Flask, render_template, request, redirect, url_for, session
import os
from database import init_db, save_meeting, get_all_meetings, is_slot_available
from email_service import send_confirmation_email

app = Flask(__name__)

# =========================
# 🔐 ENV VARIABLES
# =========================
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


# =========================
# INIT DATABASE (SAFE FOR RENDER)
# =========================
@app.before_first_request
def setup():
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print("DB INIT ERROR:", e)


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template("booking.html")


# =========================
# BOOK MEETING
# =========================
@app.route('/book', methods=['POST'])
def book():
    try:
        # Safe form handling
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        # Validate input
        if not name or not email or not date or not time:
            return "ERROR: Missing form data"

        # Check slot availability
        if not is_slot_available(date, time):
            return "This time slot is already booked."

        # TEMP meet link
        meet_link = "https://meet.google.com/test-link"

        # Save to database
        save_meeting(name, email, date, time, meet_link)

        # Send email safely
        try:
            send_confirmation_email(email, name, date, time, meet_link)
        except Exception as e:
            print("Email error:", e)

        return render_template("success.html",
                               name=name,
                               date=date,
                               time=time,
                               meet_link=meet_link)

    except Exception as e:
        return f"ERROR OCCURRED: {str(e)}"


# =========================
# LOGIN ROUTE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials"

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
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

