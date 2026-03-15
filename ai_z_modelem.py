import os
import shutil
import json
import numpy as np
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import sys

print("🤖 AI - START")

folder = 'zdjecia_czekajace'
pliki = os.listdir(folder)

zdjecia = [p for p in pliki if p.endswith(('.jpg', '.png', '.jpeg'))]

if not zdjecia:
    print("Brak zdjec")
    sys.exit(0)

zdjecie = zdjecia
print(f"Zdjecie: {zdjecie}")

sciezka = os.path.join(folder, zdjecie)

model = load_model('model.h5')

img = cv2.imread(sciezka)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (224, 224))
img = img.astype(np.float32) / 255.0
img = np.expand_dims(img, axis=0)

wynik = model.predict(img, verbose=0)
plate_number = str(wynik)

print(f"Rozpoznano: {plate_number}")

if os.path.exists('data/parking.json'):
    with open('data/parking.json') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": "", "status": "wolne", "czas": ""} for i in range(1, 7)]

for m in parking:
    if m['status'] == 'wolne':
        m['status'] = 'zajete'
        m['blacha'] = plate_number
        m['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        break

os.makedirs('data', exist_ok=True)
with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
shutil.move(sciezka, os.path.join('zdjecia_gotowe', nowa_nazwa))

print("GOTOWE")
