from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "rahul_event_secret_2026"

services_data = [
    {"title": "Wedding Decoration", "desc": "Royal wedding stage, mandap, lighting in Nagpur", "img": "wedding.jpg"},
    {"title": "Birthday Decoration", "desc": "Theme birthday, balloon, kids party decoration", "img": "birthday.jpg"},
    {"title": "Stage Decoration", "desc": "Cultural, corporate stage setup", "img": "stage.jpg"},
    {"title": "Lighting & Sound", "desc": "DJ, LED lights, sound system", "img": "light.jpg"},
]
gallery_data = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg", "img5.jpg", "img6.jpg"]

@app.route('/')
def home():
    return render_template('index.html', services=services_data, gallery=gallery_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html', services=services_data)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', gallery=gallery_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/contact', methods=['POST'])
def contact_form():
    flash("Thank you! Rahul will call you soon!", "success")
    return redirect(url_for('home'))

@app.route('/book', methods=['POST'])
def book():
    flash("Booking received!", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)