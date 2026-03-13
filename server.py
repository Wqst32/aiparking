from flask import Flask, request
import cv2

app = Flask(__name__)

@app.route("/")
def home():
    return "AI parking działa"

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["image"]
    file.save("image.jpg")

    # tutaj AI analizuje zdjęcie

    return "ok"
cursor = db.cursor()
cursor.execute("SELECT 1")

print("POLACZENIE Z BAZA DZIALA")

app.run(host="0.0.0.0", port=8080)
