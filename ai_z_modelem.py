import os
import shutil
import json
import numpy as np
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import sys
import re

print("🤖 AI OCR - ODCZYT TABLIC - START")

# 1. Znajdź zdjęcie w czekajace
zdjecia = [f for f in os.listdir('zdjecia_czekajace') if f.endswith('.jpg')]
if not zdjecia:
    print("❌ Brak zdjęć w zdjecia_czekajace")
    sys.exit(0)

zdjecie = zdjecia[0]
sciezka_zdjecia = os.path.join('zdjecia_czekajace', zdjecie)
print(f"📸 Analizuję: {zdjecie}")

# 2. Wczytaj model
print("🔄 Ładowanie model.h5...")
if not os.path.exists('model.h5'):
    print("❌ BRAK PLIKU model.h5 w repozytorium!")
    sys.exit(1)

model = load_model('model.h5')
print("✅ Model załadowany")

# 3. Przetwórz zdjęcie (dostosuj do swojego modelu!)
print("🔧 Przetwarzanie zdjęcia...")
img = cv2.imread(sciezka_zdjecia)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (224, 224))  # Zmień jeśli Twój model wymaga innego rozmiaru
img = img.astype(np.float32) / 255.0
img = np.expand_dims(img, axis=0)

# 4. Wykonaj predykcję
print("🤖 AI odczytuje tablicę...")
wynik = model.predict(img, verbose=0)

# 5. INTERPRETACJA - model zwraca TEKST (np. "WAW123")
# To zależy jak trenowałeś model - może zwracać:
# - string
# - listę znaków
# - zakodowaną wartość

print(f"📊 Surowe wyjście modelu: {wynik}")
print(f"📊 Typ wyniku: {type(wynik)}")
print(f"📊 Kształt: {wynik.shape if hasattr(wynik, 'shape') else 'brak'}")

# PRÓBA 1: Jeśli model zwraca string bezpośrednio
try:
    if isinstance(wynik, str):
        plate_number = wynik.strip()
    elif isinstance(wynik, bytes):
        plate_number = wynik.decode('utf-8').strip()
    elif hasattr(wynik, 'numpy'):  # TensorFlow tensor
        plate_number = str(wynik.numpy())
    elif isinstance(wynik, np.ndarray):
        # Jeśli to tablica znaków
        if wynik.dtype.type is np.str_ or wynik.dtype.type is np.object_:
            plate_number = ''.join([chr(x) if isinstance(x, np.uint8) else str(x) for x in wynik.flatten()])
        else:
            plate_number = str(wynik[0][0])
    else:
        plate_number = str(wynik)
except:
    plate_number = "ERROR_ODCZYTU"

# Wyczyść wynik - zostaw tylko litery i cyfry
plate_number = re.sub(r'[^A-Za-z0-9]', '', plate_number)
print(f"✅ ODCZYTANO TABLICĘ: {plate_number}")

# 6. Wczytaj parking
if os.path.exists('data/parking.json'):
    with open('data/parking.json') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": f"Miejsce {i}", "status": "wolne", "czas": ""} 
               for i in range(1, 7)]

# 7. Zajmij pierwsze wolne
for miejsce in parking:
    if miejsce['status'] == 'wolne':
        miejsce['status'] = 'zajete'
        miejsce['blacha'] = plate_number
        miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        print(f"✅ Zajęto miejsce {miejsce['id']} tablicą {plate_number}")
        break

# 8. Zapisz parking
with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

# 9. Przenieś zdjęcie
os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
shutil.move(sciezka_zdjecia, os.path.join('zdjecia_gotowe', nowa_nazwa))
print(f"📦 Przeniesiono do: zdjecia_gotowe/{nowa_nazwa}")

print("✅ KONIEC")
