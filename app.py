from flask import Flask, render_template, request
import traceback

app = Flask(__name__)


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    try:
        return render_template("booking.html")
    except Exception as e:
        return f"HOME ERROR: {str(e)}"


# =========================
# BOOK ROUTE (FULL DEBUG)
# =========================
@app.route('/book', methods=['POST'])
def book():
    try:
        print("---- BOOK ROUTE HIT ----")

        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        print("FORM DATA:", name, email, date, time)

        # Simple return (NO DB, NO EMAIL)
        return f"""
        <h2>SUCCESS ✅</h2>
        <p>Name: {name}</p>
        <p>Email: {email}</p>
        <p>Date: {date}</p>
        <p>Time: {time}</p>
        """

    except Exception as e:
        error_trace = traceback.format_exc()
        return f"""
        <h2>ERROR ❌</h2>
        <pre>{error_trace}</pre>
        """


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

