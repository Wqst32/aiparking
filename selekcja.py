import cv2
import os
import shutil
from datetime import datetime
import hashlib

def ocen_ostrosc(sciezka):
    """Ocenia ostrość zdjęcia w skali 0-100"""
    try:
        img = cv2.imread(sciezka, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        return min(100, laplacian.var() / 10)
    except Exception as e:
        print(f"Błąd oceny {sciezka}: {e}")
        return 0

def znajdz_serie_zdjec():
    """Grupuje zdjęcia które przyszły w odstępie < 3 minut"""
    zdjecia = [f for f in os.listdir('zdjecia') 
               if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not zdjecia:
        return []
    
    # Sortuj po czasie utworzenia
    zdjecia.sort(key=lambda x: os.path.getmtime(os.path.join('zdjecia', x)))
    
    serie = []
    obecna_seria = []
    ostatni_czas = None
    
    for zdj in zdjecia:
        sciezka = os.path.join('zdjecia', zdj)
        czas = os.path.getmtime(sciezka)
        
        if ostatni_czas is None or (czas - ostatni_czas) < 180:  # 3 minuty
            obecna_seria.append(zdj)
        else:
            if len(obecna_seria) >= 3:
                serie.append(obecna_seria)
            obecna_seria = [zdj]
        
        ostatni_czas = czas
    
    if len(obecna_seria) >= 3:
        serie.append(obecna_seria)
    
    return serie

def main():
    print("\n" + "="*60)
    print("🔍 SELEKCJA ZDJĘĆ - START")
    print("="*60)
    
    # Stwórz potrzebne foldery
    os.makedirs('zdjecia_czekajace', exist_ok=True)
    
    # Znajdź serie zdjęć
    serie = znajdz_serie_zdjec()
    print(f"Znaleziono {len(serie)} serii zdjęć")
    
    for i, seria in enumerate(serie):
        print(f"\n--- Seria {i+1}: {len(seria)} zdjęć ---")
        
        # Oceń każde zdjęcie
        oceny = []
        for zdj in seria:
            sciezka = os.path.join('zdjecia', zdj)
            ostrosc = ocen_ostrosc(sciezka)
            oceny.append((zdj, sciezka, ostrosc))
            print(f"  {zdj}: ostrość {ostrosc:.1f}")
        
        # Wybierz najlepsze
        najlepsze = max(oceny, key=lambda x: x[2])
        print(f"\n✅ WYBRANO: {najlepsze[0]} (ostrość: {najlepsze[2]:.1f})")
        
        # Generuj unikalną nazwę
        data = datetime.now().strftime('%Y%m%d_%H%M%S')
        nowa_nazwa = f"seria_{i+1}_{data}.jpg"
        cel = os.path.join('zdjecia_czekajace', nowa_nazwa)
        
        # Przenieś najlepsze
        shutil.move(najlepsze[1], cel)
        print(f"📦 Przeniesiono do: zdjecia_czekajace/{nowa_nazwa}")
        
        # Usuń resztę
        for zdj, sciezka, _ in oceny:
            if zdj != najlepsze[0] and os.path.exists(sciezka):
                os.remove(sciezka)
                print(f"🗑️ Usunięto: {zdj}")
    
    print("\n" + "="*60)
    print("✅ SELEKCJA ZAKOŃCZONA")
    print("="*60)

if __name__ == "__main__":
    main()
