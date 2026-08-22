from flask import Flask, render_template, request, session, redirect
import mysql.connector, os
app = Flask(__name__)
app.secret_key = "rahul_event_secret_key"
db = mysql.connector.connect(host="localhost", user="root", password="Sonali@2007", database="rahul_events")
cursor = db.cursor(buffered=True)

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
        cursor.execute("INSERT INTO enquiries (full_name, email, mobile, subject, message) VALUES (%s,%s,%s,%s,%s)", (request.form["full_name"], request.form["email"], request.form["mobile"], request.form["subject"], request.form["message"]))
        db.commit()
        return "Enquiry Submitted!"
    return render_template("contact.html")
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        cursor.execute("INSERT INTO bookings (full_name, mobile, email, event_type, event_date, event_time, event_address, decoration_requirements, additional_message, booking_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')", (request.form["full_name"], request.form["mobile"], request.form["email"], request.form["event_type"], request.form["event_date"], request.form["event_time"], request.form["event_address"], request.form["decoration_requirements"], request.form["additional_message"]))
        db.commit()
        return "Booking Submitted!"
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
    cursor.execute("SELECT * FROM bookings ORDER BY booking_id DESC")
    bookings=cursor.fetchall()
    cursor.execute("SELECT * FROM enquiries ORDER BY enquiry_id DESC")
    enquiries=cursor.fetchall()
    return render_template("admin.html", bookings=bookings, enquiries=enquiries)
@app.route("/update_status/<int:id>/<string:new_status>")
def update_status(id, new_status):
    cursor.execute("UPDATE bookings SET booking_status=%s WHERE booking_id=%s", (new_status, id))
    db.commit()
    return redirect("/admin")
@app.route("/delete_booking/<int:id>")
def delete_booking(id):
    cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (id,))
    db.commit()
    return redirect("/admin")
@app.route("/read_enquiry/<int:id>")
def read_enquiry(id):
    cursor.execute("UPDATE enquiries SET status='Read' WHERE enquiry_id=%s", (id,))
    db.commit()
    return redirect("/admin")
@app.route("/delete_enquiry/<int:id>")
def delete_enquiry(id):
    cursor.execute("DELETE FROM enquiries WHERE enquiry_id=%s", (id,))
    db.commit()
    return redirect("/admin")
@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin-login")
if __name__ == "__main__":
    app.run(debug=True)