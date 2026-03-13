from flask import Flask
import mysql.connector

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="mysql://root:mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD@mysql.railway.internal:3306/railway",
        user="root",
        password="mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD",
        database="parking"
    )

@app.route("/update")
def update_db():

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("UPDATE parking SET status='test' WHERE id=1")
    db.commit()

    return "baza zmieniona"

print("SERVER START")
import mysql.connector

print("SERVER START")

db = mysql.connector.connect(
        host="mysql://root:mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD@mysql.railway.internal:3306/railway",
        user="root",
        password="mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD",
        database="parking"
)

cursor = db.cursor()
cursor.execute("UPDATE parking SET status='test' WHERE id=1")
db.commit()

print("ZMIENIONO BAZE")

app.run(host="0.0.0.0", port=8080)
