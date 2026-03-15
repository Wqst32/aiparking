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
folder = 'zdjecia_czekajace'
if not os.path.exists(folder):
    print(f"❌ Brak folderu {folder}")
    sys.exit(1)

pliki = os.listdir(folder)
print(f"Wszystkie pliki: {pliki}")

# Filtruj tylko zdjęcia
zdjecia = []
for plik in pliki:
    if plik.endswith('.jpg') or plik.endswith('.png') or plik.endswith('.jpeg'):
        zdjecia.append(plik)

print(f"Znalezione zdjęcia: {zdjecia}")

if len(zdjecia) == 0:
    print("❌ Brak zdjęć")
    sys.exit(0)

# Weź PIERWSZE zdjęcie
zdjecie = zdjecia
print(f"📸 Wybrane: {zdjecie}")
print(f"Typ: {type(zdjecie)}")

sciezka = os.path.join(folder, zdjecie)
print(f"Ścieżka: {sciezka}")

# 2. Wczytaj model
print("🔄 Ładowanie modelu...")
try:
    model = load_model('model.h5')
    print("✅ Model załadowany")
except Exception as e:
    print(f"❌ Błąd: {e}")
    sys.exit(1)

# 3. Przetwórz zdjęcie
print("🔧 Przetwarzanie zdjęcia...")
try:
    img = cv2.imread(sciezka)
    if img is None:
        print(f"❌ Nie można wczytać: {sciezka}")
        sys.exit(1)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    print("✅ Zdjęcie gotowe")
except Exception as e:
    print(f"❌ Błąd: {e}")
    sys.exit(1)

# 4. Predykcja
print("🤖 Predykcja...")
try:
    wynik = model.predict(img, verbose=0)
    plate_number = str(wynik)
    print(f"✅ Rozpoznano: {plate_number}")
except Exception as e:
    print(f"❌ Błąd: {e}")
    plate_number = "ERROR"

# 5. Aktualizuj parking.json
print("📝 Aktualizacja parkingu...")
if os.path.exists('data/parking.json'):
    with open('data/parking.json', 'r') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": "", "status": "wolne", "czas": ""} for i in range(1, 7)]

for miejsce in parking:
    if miejsce['status'] == 'wolne':
        miejsce['status'] = 'zajete'
        miejsce['blacha'] = plate_number
        miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        print(f"✅ Miejsce {miejsce['id']} zajęte")
        break

os.makedirs('data', exist_ok=True)
with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

# 6. Przenieś zdjęcie
print("📦 Przenoszenie zdjęcia...")
os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
nowa_sciezka = os.path.join('zdjecia_gotowe', nowa_nazwa)
shutil.move(sciezka, nowa_sciezka)
print(f"✅ Przeniesiono do: {nowa_sciezka}")
