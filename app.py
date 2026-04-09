from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, save_meeting, get_all_meetings, is_slot_available
from email_service import send_confirmation_email

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

# Initialize database
init_db()


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template("booking.html")


# =========================
# BOOK MEETING (FIXED)
# =========================
@app.route('/book', methods=['POST'])
def book():
    try:
        # 🔹 STEP 1: Get data
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        print("STEP 1: Data received")
        print(name, email, date, time)

        # 🔹 STEP 2: Check slot
        if not is_slot_available(date, time):
            print("Slot already booked")
            return "This slot is already booked"

        # 🔹 STEP 3: Create meet link (temporary)
        meet_link = "https://meet.google.com/new"

        # 🔹 STEP 4: Save to DB
        print("STEP 2: Saving meeting")
        save_meeting(name, email, date, time, meet_link)

        # 🔹 STEP 5: Send email
        print("STEP 3: Calling email function")
        send_confirmation_email(email, name, date, time, meet_link)
        print("STEP 4: Email function DONE")

        # 🔹 STEP 6: Show success page
        return render_template("success.html",
                               name=name,
                               date=date,
                               time=time,
                               meet_link=meet_link)

    except Exception as e:
        print("❌ ERROR IN /book:", str(e))
        return "Something went wrong. Please try again."


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "admin123":
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




