import os
import sys

print("🤖 TEST - START")

# Sprawdź czy są zdjęcia
if not os.path.exists('zdjecia_czekajace'):
    print("❌ Brak folderu zdjecia_czekajace")
    sys.exit(1)

zdjecia = os.listdir('zdjecia_czekajace')
print(f"📸 Znalezione pliki: {zdjecia}")

if not zdjecia:
    print("❌ Brak plików")
    sys.exit(1)

print("✅ TEST OK")
