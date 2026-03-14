import json
import os
import random
from datetime import datetime

# Lista przykładowych tablic do losowania
TABLICE = ["WAW123", "KRK456", "GDN789", "POZ111", "WRO222", "LUB333", "RZE777", "OPO888"]

def znajdz_najnowsze_zdjecie():
    """Znajduje najnowsze zdjęcie w folderze zdjecia/"""
    zdjecia = [f for f in os.listdir('zdjecia') 
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not zdjecia:
        return None
    
    # Sortuj według daty utworzenia
    zdjecia.sort(key=lambda x: os.path.getmtime(f'zdjecia/{x}'), reverse=True)
    return zdjecia[0]

def aktualizuj_parking(tablica):
    """Aktualizuje parking.json"""
    
    # Wczytaj obecny parking
    with open('data/parking.json', 'r') as f:
        parking = json.load(f)
    
    # Znajdź pierwsze wolne miejsce
    for miejsce in parking:
        if miejsce['status'] == 'wolne':
            miejsce['status'] = 'zajete'
            miejsce['blacha'] = tablica
            miejsce['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
            print(f"✅ Zajęto miejsce {miejsce['id']} tablicą {tablica}")
            break
    
    # Zapisz zmiany
    with open('data/parking.json', 'w') as f:
        json.dump(parking, f, indent=2)

def main():
    print("🔍 Szukam nowego zdjęcia...")
    zdjecie = znajdz_najnowsze_zdjecie()
    
    if not zdjecie:
        print("❌ Brak zdjęć")
        return
    
    print(f"📸 Znaleziono zdjęcie: {zdjecie}")
    
    # TU BĘDZIE PRAWDZIWE AI W PRZYSZŁOŚCI
    # Na razie losujemy tablicę
    wylosowana_tablica = random.choice(TABLICE)
    print(f"🤖 AI rozpoznało tablicę: {wylosowana_tablica}")
    
    aktualizuj_parking(wylosowana_tablica)
    print("✨ Gotowe!")

if __name__ == "__main__":
    main()
