import os
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "rahul_event_secret_key_2024"

# Email Config - Tujha email
EMAIL_SENDER = "rahuleventcreations2007@gmail.com"
EMAIL_PASSWORD = "dkgf ybyv qvbm ybqo"  # Tujha App Password
OWNER_EMAILS = ["rahuleventcreations2007@gmail.com", "sonali2007-code@gmail.com"]

# --- FIXED EMAIL FUNCTION ---
def send_email_async(to_list, subject, html_body):
    def _send():
        try:
            recipients = to_list if isinstance(to_list, list) else [to_list]
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(html_body, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipients, msg.as_string())
            server.quit()
            print(f"Email sent to {recipients}")
        except Exception as e:
            print(f"Email Error: {e}")
    threading.Thread(target=_send).start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services(): 
    return render_template("services.html")

@app.route("/gallery")
def gallery():
    img = os.path.join(app.root_path, 'static', 'images')
    vid = os.path.join(app.root_path, 'static', 'videos')
    images = sorted(os.listdir(img)) if os.path.exists(img) else []
    videos = sorted(os.listdir(vid)) if os.path.exists(vid) else []
    return render_template("gallery.html", images=images, videos=videos)

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        event = request.form.get("event")
        date = request.form.get("date")
        
        html_body = f"""
        <h2>New Booking - Rahul Event Creations</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Event:</b> {event}</p>
        <p><b>Date:</b> {date}</p>
        """
        send_email_async(OWNER_EMAILS, f"New Booking from {name}", html_body)
        flash("Booking Successful! We will contact you soon.", "success")
        return redirect(url_for("home"))
    return render_template("booking.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "Sona11@2007":
            session['logged_in'] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong Password!", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
