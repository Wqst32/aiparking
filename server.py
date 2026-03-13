from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/update")
def update():

    db = mysql.connector.connect(
        host="HOST",
        user="USER",
        password="PASSWORD",
        database="DATABASE"
    )

    cursor = db.cursor()
    cursor.execute("UPDATE parking SET status='test' WHERE id=1")
    db.commit()

    return "OK"

app.run(host="0.0.0.0", port=8080)
