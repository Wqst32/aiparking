import os
import shutil
import json
import random
from datetime import datetime

print("🤖 AI START")

# 1. Znajdź zdjęcie w czekajace
zdjecia = [f for f in os.listdir('zdjecia_czekajace') if f.endswith('.jpg')]
if not zdjecia:
    print("Brak zdjęć")
    exit(0)

zdjecie = zdjecia[0]
sciezka = os.path.join('zdjecia_czekajace', zdjecie)
print(f"📸 Analizuję: {zdjecie}")

# 2. Symulacja AI - losuj tablicę
tablica = random.choice(["WAW123", "KRK456", "GDN789", "POZ111"])
print(f"✅ Rozpoznano: {tablica}")

# 3. Wczytaj parking
if os.path.exists('data/parking.json'):
    with open('data/parking.json') as f:
        parking = json.load(f)
else:
    parking = [{"id": i, "blacha": f"Miejsce {i}", "status": "wolne", "czas": ""} 
               for i in range(1, 7)]

# 4. Zajmij pierwsze wolne
for miejsce in parking:
    if miejsce['status'] == 'wolne':
        miejsce['status'] = 'zajete'
        miejsce['blacha'] = tablica
        miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
        print(f"✅ Zajęto miejsce {miejsce['id']}")
        break

# 5. Zapisz parking
with open('data/parking.json', 'w') as f:
    json.dump(parking, f, indent=2)

# 6. Przenieś zdjęcie do gotowe
os.makedirs('zdjecia_gotowe', exist_ok=True)
nowa_nazwa = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tablica}.jpg"
shutil.move(sciezka, os.path.join('zdjecia_gotowe', nowa_nazwa))
print(f"📦 Przeniesiono do: zdjecia_gotowe/{nowa_nazwa}")
print("✅ Koniec")
