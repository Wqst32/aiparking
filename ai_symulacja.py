import os
import shutil
import json
import random
from datetime import datetime

import sys
print("🚀 AI SYMULACJA - START")
print(f"Argumenty: {sys.argv}")
print(f"Katalog bieżący: {os.getcwd()}")
print(f"Pliki w katalogu: {os.listdir('.')}")

# Lista możliwych tablic (do symulacji)
TABLICE_REJESTRACYJNE = [
    "WAW12345", "KRK67890", "GDN54321", "POZ98765",
    "WRO24680", "LOD13579", "SZC11223", "BYG44556",
    "RZE77889", "OPO99001", "ZGB33445", "LUB55667"
]

def wczytaj_lub_stworz_parking():
    """Wczytuje parking.json lub tworzy nowy jeśli nie istnieje"""
    if os.path.exists('data/parking.json'):
        with open('data/parking.json', 'r') as f:
            return json.load(f)
    else:
        # Stwórz domyślny parking
        parking = []
        for i in range(1, 7):
            parking.append({
                "id": i,
                "blacha": f"Miejsce {i}",
                "status": "wolne",
                "czas": ""
            })
        return parking

def zapisz_parking(parking):
    """Zapisuje parking.json"""
    os.makedirs('data', exist_ok=True)
    with open('data/parking.json', 'w') as f:
        json.dump(parking, f, indent=2, ensure_ascii=False)

def znajdz_wolne_miejsce(parking):
    """Znajduje pierwsze wolne miejsce"""
    for miejsce in parking:
        if miejsce['status'] == 'wolne':
            return miejsce
    return None

def symuluj_rozpoznawanie_tablicy(nazwa_zdjecia):
    """
    SYMULACJA AI - zwraca losową tablicę
    PÓŹNIEJ ZASTĄPISZ TO PRAWDZIWYM MODELEM (model.h5)
    """
    # Możesz wykorzystać nazwę pliku do symulacji
    if "test" in nazwa_zdjecia.lower():
        return "TEST12345"
    
    return random.choice(TABLICE_REJESTRACYJNE)

def main():
    print("\n" + "="*60)
    print("🤖 AI - ROZPOZNAWANIE TABLIC")
    print("="*60)
    
    # Sprawdź czy są zdjęcia do analizy
    if not os.path.exists('zdjecia_czekajace'):
        os.makedirs('zdjecia_czekajace', exist_ok=True)
        print("Brak zdjęć do analizy")
        return
    
    zdjecia = [f for f in os.listdir('zdjecia_czekajace') 
               if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not zdjecia:
        print("Brak zdjęć do analizy")
        return
    
    print(f"Znaleziono {len(zdjecia)} zdjęć do analizy")
    
    # Wczytaj parking
    parking = wczytaj_lub_stworz_parking()
    
    # Przetwarzaj każde zdjęcie
    for zdjecie in zdjecia:
        print(f"\n📸 Analizuję: {zdjecie}")
        
        sciezka = os.path.join('zdjecia_czekajace', zdjecie)
        
        # Krok 1: Symulacja AI - rozpoznaj tablicę
        print("   🔍 AI pracuje...")
        tablica = symuluj_rozpoznawanie_tablicy(zdjecie)
        print(f"   ✅ Rozpoznano tablicę: {tablica}")
        
        # Krok 2: Znajdź wolne miejsce
        wolne = znajdz_wolne_miejsce(parking)
        
        if wolne:
            # Zajmij miejsce
            wolne['status'] = 'zajete'
            wolne['blacha'] = tablica
            wolne['czas'] = datetime.now().strftime('%H:%M %d.%m.%Y')
            print(f"   ✅ Zajęto miejsce nr {wolne['id']}")
            
            # Krok 3: Przenieś do archiwum
            os.makedirs('zdjecia_gotowe', exist_ok=True)
            data = datetime.now().strftime('%Y%m%d_%H%M%S')
            nowa_nazwa = f"{data}_{tablica}.jpg"
            shutil.move(sciezka, os.path.join('zdjecia_gotowe', nowa_nazwa))
            print(f"   📦 Archiwum: zdjecia_gotowe/{nowa_nazwa}")
        else:
            print("   ❌ Brak wolnych miejsc!")
            # Jeśli brak miejsc, przenieś do osobnego folderu
            os.makedirs('zdjecia_odrzucone', exist_ok=True)
            shutil.move(sciezka, os.path.join('zdjecia_odrzucone', zdjecie))
    
    # Zapisz zaktualizowany parking
    zapisz_parking(parking)
    print("\n✅ Zapisano parking.json")
    
    # Podsumowanie
    wolne = sum(1 for m in parking if m['status'] == 'wolne')
    zajete = 6 - wolne
    print(f"\n📊 Podsumowanie: {wolne} wolnych, {zajete} zajętych")
    
    print("\n" + "="*60)
    print("✅ AI ZAKOŃCZYŁO PRACĘ")
    print("="*60)

if __name__ == "__main__":
    main()
