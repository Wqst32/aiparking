from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/wjazd")
def wjazd():

    db = mysql.connector.connect(
        host="mysql://root:mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD@mysql.railway.internal:3306/railway",
        user="root",
        password="mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD",
        database="parking"
    )

    cursor = db.cursor()
    cursor.execute("INSERT INTO parking (tablica, czas) VALUES ('TEST123', NOW())")
    db.commit()

    return "dodano"

app.run(host="0.0.0.0", port=8080)
