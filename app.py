import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv(override=True)

app = Flask(__name__)

def get_db():
    import mysql.connector
    return mysql.connector.connect(
        host=os.getenv("DB_HOST","").strip(),
        port=int(os.getenv("DB_PORT","28752")),
        user=os.getenv("DB_USER","").strip(),
        password=os.getenv("DB_PASSWORD","").strip(),
        database=os.getenv("DB_NAME","").strip(),
        ssl_ca=os.path.join(os.path.dirname(__file__), "ca.pem")
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("index.html")

@app.route("/booking", methods=["GET","POST"])
def booking():
    if request.method == "POST":
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS bookings (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), phone VARCHAR(20), event_type VARCHAR(100), event_date DATE, message TEXT)")
            cur.execute("INSERT INTO bookings (name,phone,event_type,event_date,message) VALUES (%s,%s,%s,%s,%s)",
                (request.form.get("name"), request.form.get("phone"), request.form.get("event_type"), request.form.get("event_date"), request.form.get("message")))
            conn.commit()
            cur.close()
            conn.close()
            return "<h1 style='color:green;text-align:center;margin-top:50px'>Booking Successful!</h1><a href='/' style='display:block;text-align:center'>Go Home</a>"
        except Exception as e:
            return f"Error: {e} <a href='/'>Home</a>"
    return render_template("booking.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)