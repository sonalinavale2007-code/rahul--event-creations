from flask import Flask, render_template, request, session, redirect
import mysql.connector, os, smtplib, threading, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "rahul_event_secret_key"

# --- CONFIG ---
EMAIL_SENDER = "rahulevent07@gmail.com"
EMAIL_PASSWORD = "dkqfrwyypkgtovbv"  # space kadhle aahet
OWNER_EMAILS = ["rj475201@gmail.com", "rahulevent07@gmail.com"]

try:
    db = mysql.connector.connect(host="localhost", user="root", password="Sonali@2007", database="rahul_events")
    cursor = db.cursor(buffered=True)
except:
    db = None
    cursor = None

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
def home(): return render_template("index.html")
@app.route("/services")
def services(): return render_template("services.html")
@app.route("/gallery")
def gallery():
    img = os.path.join(app.root_path, 'static', 'images')
    vid = os.path.join(app.root_path, 'static', 'videos')
    images = sorted(os.listdir(img)) if os.path.exists(img) else []
    videos = sorted(os.listdir(vid)) if os.path.exists(vid) else []
    return render_template("gallery.html", images=images, videos=videos)
@app.route("/about")
def about(): return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["full_name"]; email = request.form["email"]; mobile = request.form["mobile"]; subj = request.form["subject"]; msg = request.form["message"]
        try:
            if cursor and db:
                cursor.execute("INSERT INTO enquiries (full_name, email, mobile, subject, message) VALUES (%s,%s,%s,%s,%s)", (name, email, mobile, subj, msg))
                db.commit()
        except: pass
        html = f"<h3>New Enquiry from {name}</h3><p><b>Mobile:</b> {mobile}<br><b>Email:</b> {email}<br><b>Subject:</b> {subj}<br><b>Message:</b> {msg}</p>"
        send_email_async(OWNER_EMAILS, f"New Enquiry: {subj} - {name}", html)
        return "<h2 style='text-align:center;margin-top:50px;'>Enquiry Submitted! We will contact you soon.</h2>"
    return render_template("contact.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        d = {k: request.form.get(k) for k in ["full_name","mobile","email","event_type","event_date","event_time","event_address","decoration_requirements","additional_message"]}
        try:
            if cursor and db:
                cursor.execute("INSERT INTO bookings (full_name, mobile, email, event_type, event_date, event_time, event_address, decoration_requirements, additional_message, booking_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')", (d["full_name"], d["mobile"], d["email"], d["event_type"], d["event_date"], d["event_time"], d["event_address"], d["decoration_requirements"], d["additional_message"]))
                db.commit()
        except Exception as e: print(e)
        
        owner_html = f"<h2>🎉 New Booking!</h2><p><b>Name:</b> {d['full_name']}<br><b>Mobile:</b> {d['mobile']}<br><b>Email:</b> {d['email']}<br><b>Event:</b> {d['event_type']}<br><b>Date:</b> {d['event_date']} at {d['event_time']}<br><b>Address:</b> {d['event_address']}<br><b>Req:</b> {d['decoration_requirements']}<br><b>Msg:</b> {d['additional_message']}</p>"
        send_email_async(OWNER_EMAILS, f"New Booking: {d['event_type']} - {d['full_name']}", owner_html)
        
        cust_html = f"<h3>Thank you {d['full_name']}!</h3><p>Your booking for <b>{d['event_type']}</b> on <b>{d['event_date']}</b> is received. Rahul Events will call you soon.</p><p>📞 7350560075</p>"
        send_email_async(d['email'], "Booking Received - Rahul Event Creations", cust_html)
        
        return "<h2 style='text-align:center;margin-top:50px;'>Booking Submitted! Thank you!</h2>"
    return render_template("booking.html")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"]=="rahul" and request.form["password"]=="Rahul@123":
            session["admin_logged_in"]=True
            return redirect("/admin")
    return render_template("admin_login.html")
@app.route("/admin")
def admin():
    bookings=[];enquiries=[]
    try:
        if cursor and db:
            cursor.execute("SELECT * FROM bookings ORDER BY booking_id DESC")
            bookings=cursor.fetchall()
            cursor.execute("SELECT * FROM enquiries ORDER BY enquiry_id DESC")
            enquiries=cursor.fetchall()
    except: pass
    return render_template("admin.html", bookings=bookings, enquiries=enquiries)
@app.route("/update_status/<int:id>/<string:new_status>")
def update_status(id, new_status):
    try:
        if cursor and db:
            cursor.execute("UPDATE bookings SET booking_status=%s WHERE booking_id=%s", (new_status, id))
            db.commit()
    except: pass
    return redirect("/admin")
@app.route("/delete_booking/<int:id>")
def delete_booking(id):
    try:
        if cursor and db:
            cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (id,))
            db.commit()
    except: pass
    return redirect("/admin")
@app.route("/read_enquiry/<int:id>")
def read_enquiry(id):
    try:
        if cursor and db:
            cursor.execute("UPDATE enquiries SET status='Read' WHERE enquiry_id=%s", (id,))
            db.commit()
    except: pass
    return redirect("/admin")
@app.route("/delete_enquiry/<int:id>")
def delete_enquiry(id):
    try:
        if cursor and db:
            cursor.execute("DELETE FROM enquiries WHERE enquiry_id=%s", (id,))
            db.commit()
    except: pass
    return redirect("/admin")
@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin-login")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
