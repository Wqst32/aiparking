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

# 1. Znajdź zdjęcie
if not os.path.exists('zdjecia_czekajace'):
    print("❌ Brak folderu zdjecia_czekajace")
    sys.exit(1)

wszystkie_pliki = os.listdir('zdjecia_czekajace')
print(f"Wszystkie pliki: {wszystkie_pliki}")

zdjecia = [f for f in wszystkie_pliki if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
print(f"Znalezione zdjęcia: {zdjecia}")

if not zdjecia:
    print("❌ Brak zdjęć")
    sys.exit(0)

zdjecie = zdjecia  # PIERWSZY ELEMENT
print(f"📸 Plik: {zdjecie} (typ: {type(zdjecie)})")

sciezka = os.path.join('zdjecia_czekajace', zdjecie)
print(f"Ścieżka: {sciezka}")

# 2. Wczytaj model
try:
    model = load_model('model.h5')
    print("✅ Model załadowany")
except Exception as e:
    print(f"❌ Błąd modelu: {e}")
    sys.exit(1)

# 3. Przetwórz zdjęcie
try:
    img = cv2.imread(sciezka)
    if img is None:
        print(f"❌ Nie można wczytać zdjęcia: {sciezka}")
        sys.exit(1)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    print("✅ Zdjęcie przetworzono")
except Exception as e:
    print(f"❌ Błąd przetwarzania: {e}")
    sys.exit(1)

# 4. Predykcja
try:
    wynik = model.predict(img, verbose=0)
    plate_number = str(wynik)
    print(f"✅ Rozpoznano: {plate_number}")
except Exception as e:
    print(f"❌ Błąd predykcji: {e}")
    plate_number = "ERROR"

# 5. Aktualizuj parking
if os.path.exists('data/parking.json'):
    with open('data/parking.json') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": f"Miejsce {i}", "status": "wolne", "czas": ""} for i in range(1, 7)]

for miejsce in parking:
    if miejsce['status'] == 'wolne':
        miejsce['status'] = 'zajete'
        miejsce['blacha'] = plate_number
        miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        print(f"✅ Zajęto miejsce {miejsce['id']}")
        break

with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

# 6. Przenieś zdjęcie
os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
stara_sciezka = sciezka
nowa_sciezka = os.path.join('zdjecia_gotowe', nowa_nazwa)
