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
