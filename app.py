from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "rahul_event_secret_2026"

# --- Data for Website ---
services_data = [
    {"title": "Wedding Decoration", "desc": "Royal wedding stage, mandap, lighting in Nagpur", "img": "wedding.jpg"},
    {"title": "Birthday Decoration", "desc": "Theme birthday, balloon, kids party decoration", "img": "birthday.jpg"},
    {"title": "Stage Decoration", "desc": "Cultural, corporate stage setup", "img": "stage.jpg"},
    {"title": "Lighting & Sound", "desc": "DJ, LED lights, sound system", "img": "light.jpg"},
]

gallery_data = [
    "img1.jpg", "img2.jpg", "img3.jpg", 
    "img4.jpg", "img5.jpg", "img6.jpg"
]

@app.route('/')
def home():
    return render_template('index.html', services=services_data, gallery=gallery_data)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    print(f"New Booking: {name} - {phone} - {message}")
    # Yethe tu Google Sheet la save karu shaktes
    flash("Thank you! Rahul will call you soon!", "success")
    return redirect(url_for('home') + '#contact')

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    event_type = request.form.get('event')
    date = request.form.get('date')
    print(f"Booking: {name}, {event_type}, {date}")
    flash(f"{name}, your {event_type} booking request received!", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)