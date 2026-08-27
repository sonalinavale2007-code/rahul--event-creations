import os
import threading
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "rahul_event_secret_key_2024"

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
OWNER_EMAIL = "rahulevent07@gmail.com"

# Ultramsg Settings - Render var lavlele
ULTRAMSG_INSTANCE_ID = os.environ.get("ULTRAMSG_INSTANCE_ID", "instance189783")
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "j0bkw3zdj4p5he1d")
WHATSAPP_TO = "917350560075"  # Rahul cha number 91 sobat

def send_whatsapp_async(message):
    def _send():
        try:
            url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
            data = {
                "token": ULTRAMSG_TOKEN,
                "to": WHATSAPP_TO,
                "body": message
            }
            requests.post(url, data=data, timeout=15)
            print("WhatsApp Sent!")
        except Exception as e:
            print(f"WhatsApp Error: {e}")
    threading.Thread(target=_send).start()

def send_email_async(subject, html_body):
    def _send():
        try:
            if not RESEND_API_KEY: return
            data = {
                "from": "Rahul Events <onboarding@resend.dev>",
                "to": [OWNER_EMAIL],
                "subject": subject,
                "html": html_body
            }
            requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                json=data,
                timeout=10
            )
        except Exception as e:
            print(f"Error: {e}")
    threading.Thread(target=_send).start()

@app.route("/")
def home(): return render_template("index.html")
@app.route("/services")
def services(): return render_template("services.html")
@app.route("/gallery")
def gallery():
    img_path = os.path.join(app.root_path, 'static', 'images')
    vid_path = os.path.join(app.root_path, 'static', 'videos')
    images = sorted(os.listdir(img_path)) if os.path.exists(img_path) else []
    videos = sorted(os.listdir(vid_path)) if os.path.exists(vid_path) else []
    return render_template("gallery.html", images=images, videos=videos)
@app.route("/about")
def about(): return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name") or request.form.get("full_name") or "Customer"
        phone = request.form.get("phone") or request.form.get("mobile") or "No Number"
        email = request.form.get("email") or ""
        msg = request.form.get("message") or request.form.get("decoration_requirements") or ""
        
        whatsapp_msg = f"🔔 *New Contact Enquiry*\n\n*Name:* {name}\n*Phone:* {phone}\n*Email:* {email}\n*Message:* {msg}"
        send_whatsapp_async(whatsapp_msg)
        
        html = f"<h2>New Contact Enquiry</h2><p><b>Name:</b> {name}</p><p><b>Phone:</b> {phone}</p><p><b>Email:</b> {email}</p><p><b>Message:</b> {msg}</p>"
        send_email_async(f"New Contact: {name}", html)
        
        flash("Message Sent! We will contact you on WhatsApp soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form.get("full_name")
        phone = request.form.get("mobile")
        email = request.form.get("email")
        event = request.form.get("event_type")
        date = request.form.get("event_date")
        time = request.form.get("event_time")
        address = request.form.get("event_address")
        req = request.form.get("decoration_requirements")

        whatsapp_msg = f"🎉 *New Booking Request*\n\n*Name:* {name}\n*Phone:* {phone}\n*Email:* {email}\n*Event:* {event}\n*Date:* {date} at {time}\n*Address:* {address}\n*Requirement:* {req}"
        send_whatsapp_async(whatsapp_msg)

        html = f"<h2>New Booking</h2><p><b>Name:</b> {name}</p><p><b>Phone:</b> {phone}</p><p><b>Email:</b> {email}</p><p><b>Event:</b> {event}</p><p><b>Date:</b> {date} at {time}</p><p><b>Address:</b> {address}</p><p><b>Req:</b> {req}</p>"
        send_email_async(f"New Booking: {name} - {event}", html)
        flash("Booking Successful! We will contact you on WhatsApp soon.", "success")
        return redirect(url_for("booking"))
    return render_template("booking.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == "Sona11@2007":
            session['logged_in'] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong Password!", "danger")
    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'): return redirect(url_for("login"))
    return render_template("dashboard.html")
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
