
tensorflow i keras zdjecie, idk
OK, TensorFlow/Keras - napiszę CI uniwersalny skaner:
Plik skanuj.py (wrzuć do repozytorium):
python
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import os

def przygotuj_zdjecie(sciezka):
    """
    Uniwersalne przygotowanie zdjęcia dla modelu
    """
    # Wczytaj zdjęcie
    img = cv2.imread(sciezka)
    
    if img is None:
        raise Exception(f"Nie można wczytać zdjęcia: {sciezka}")
    
    # Konwertuj BGR -> RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Zmień rozmiar na 224x224 (najpopularniejszy dla TensorFlow)
    img = cv2.resize(img, (224, 224))
    
    # Normalizacja do [0,1]
    img = img.astype(np.float32) / 255.0
    
    # Dodaj wymiar batch (1, 224, 224, 3)
    img = np.expand_dims(img, axis=0)
    
    return img

def rozpoznaj(sciezka_zdjecia):
    """
    Ładuje model i rozpoznaje tablicę
    """
    print(f"📸 Wczytywanie zdjęcia: {sciezka_zdjecia}")
    
    # Sprawdź czy model istnieje
    if not os.path.exists('model.h5'):
        raise Exception("Brak pliku model.h5 w repozytorium!")
    
    # Wczytaj model
    print("🔄 Ładowanie modelu model.h5...")
    model = load_model('model.h5')
    print("✅ Model załadowany")
    
    # Przygotuj zdjęcie
    img = przygotuj_zdjecie(sciezka_zdjecia)
    
    # Predykcja
    print("🔍 AI analizuje...")
    predictions = model.predict(img, verbose=0)
    
    # Pokaż surowe wyniki (do debugowania)
    print(f"📊 Kształt wyniku: {predictions.shape}")
    print(f"📊 Wynik: {predictions}")
    
    # INTERPRETACJA - dostosuj do swojego modelu
    if len(predictions.shape) == 2 and predictions.shape[1] > 1:
        # Klasyfikacja (wiele klas)
        klasa = np.argmax(predictions[0])
        pewnosc = predictions[0][klasa]
        print(f"📊 Klasyfikacja - klasa {klasa} z pewnością {pewnosc:.2f}")
        
        # TU WPISZ SWOJE TABLICE
        # Musisz wiedzieć która klasa odpowiada której tablicy!
        tablice = {
            0: "WAW123",
            1: "KRK456",
            2: "GDN789",
            3: "POZ111",
            4: "WRO222",
            5: "LUB333",
        }
        
        wynik = tablice.get(klasa, f"KLASA_{klasa}")
        
    elif len(predictions.shape) == 2 and predictions.shape[1] == 1:
        # Regresja lub binaryfikacja
        wartosc = predictions[0][0]
        print(f"📊 Wartość: {wartosc}")
        wynik = f"WARTOSC_{wartosc:.2f}"
        
    elif len(predictions.shape) == 1:
        # Wektor
        print(f"📊 Wektor: {predictions}")
        wynik = str(predictions[0])
        
    else:
        # Nieznany format
        wynik = "NIEZNANY_FORMAT"
    
    return wynik

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Użycie: python skanuj.py <ścieżka_do_zdjęcia>")
            sys.exit(1)
        
        sciezka = sys.argv[1]
        numer = rozpoznaj(sciezka)
        print(f"✅ Wynik: {numer}")
        
        # Wypisz sam numer (to trafi do subprocess)
        print(numer)
        
    except Exception as e:
        print(f"❌ BŁĄD: {e}")
        sys.exit(1)
Teraz ai_moj_program.py (główny skrypt):
python
import os
import shutil
import json
from datetime import datetime
import subprocess
import sys

print("🤖 AI Z MOIM MODELEM .h5")

# 1. Znajdź zdjęcie
zdjecia = [f for f in os.listdir('zdjecia_czekajace') if f.endswith('.jpg')]
if not zdjecia:
    print("Brak zdjęć")
    sys.exit(0)

zdjecie = zdjecia[0]
sciezka = os.path.join('zdjecia_czekajace', zdjecie)
print(f"📸 Zdjęcie: {zdjecie}")

# 2. Uruchom skanuj.py z modelem
print("🔍 Uruchamiam model TensorFlow...")
result = subprocess.run(['python', 'skanuj.py', sciezka], 
                        capture_output=True, text=True)

# 3. Pobierz wynik (ostatnia linia to numer tablicy)
lines = result.stdout.strip().split('\n')
plate_number = lines[-1] if lines else "ERROR"
print(f"✅ Rozpoznano: {plate_number}")

if result.stderr:
    print(f"⚠️ Ostrzeżenia: {result.stderr}")

# 4. Aktualizuj parking
if os.path.exists('data/parking.json'):
    with open('data/parking.json') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": f"Miejsce {i}", "status": "wolne", "czas": ""} 
               for i in range(1, 7)]

for miejsce in parking:
    if miejsce['status'] == 'wolne':
        miejsce['status'] = 'zajete'
        miejsce['blacha'] = plate_number
        miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        print(f"✅ Zajęto miejsce {miejsce['id']}")
        break

with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

# 5. Przenieś zdjęcie
os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
shutil.move(sciezka, os.path.join('zdjecia_gotowe', nowa_nazwa))
print(f"📦 Przeniesiono do: zdjecia_gotowe/{nowa_nazwa}")

print("✅ GOTOWE")
Plik .github/workflows/2_ai.yml (z TensorFlow):
yaml
name: 2. AI - rozpoznawanie tablic

on:
  push:
    paths:
      - 'zdjecia_czekajace/*.jpg'

jobs:
  ai:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout
