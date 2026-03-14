<script>
        async function fetchParkingData() {
            try {
                const response = await fetch('api/get_parking.php');
                
                // Najpierw sprawdźmy co zwraca serwer
                const text = await response.text();
                console.log('Odpowiedź serwera (tekst):', text);
                
                // Spróbuj sparsować JSON
                try {
                    const data = JSON.parse(text);
                    console.log('Sparsowane dane:', data);
                    
                    // Ukryj błąd jeśli był
                    document.getElementById('errorMessage').style.display = 'none';
                    
                    updateParkingDisplay(data);
                    updateLastUpdateTime();
                } catch (jsonError) {
                    console.error('Błąd parsowania JSON:', jsonError);
                    document.getElementById('errorMessage').style.display = 'block';
                    document.getElementById('errorMessage').textContent = 'Błąd danych: Serwer zwrócił nieprawidłowy JSON. Sprawdź konsolę (F12).';
                    
                    // Pokaż w konsoli co zwrócił serwer
                    console.log('Treść odpowiedzi (pierwsze 200 znaków):', text.substring(0, 200));
                }
                
            } catch (error) {
                console.error('Błąd sieci:', error);
                document.getElementById('errorMessage').style.display = 'block';
                document.getElementById('errorMessage').textContent = 'Błąd połączenia: ' + error.message;
            }
        }

        function updateParkingDisplay(spots) {
            const grid = document.getElementById('parkingGrid');
            let freeCount = 0;
            let occupiedCount = 0;

            // Jeśli spots to tablica
            if (Array.isArray(spots)) {
                grid.innerHTML = spots.map(spot => {
                    if (spot.status === 'wolne') {
                        freeCount++;
                    } else {
                        occupiedCount++;
                    }

                    return `
                        <div class="parking-spot ${spot.status}">
                            <div class="spot-number">Miejsce ${spot.id}</div>
                            <div class="spot-plate">${spot.blacha || '---'}</div>
                            <div class="spot-status">${spot.status}</div>
                            <div class="spot-time">${spot.czas || '---'}</div>
                        </div>
                    `;
                }).join('');
            } else {
                grid.innerHTML = '<div class="error-message" style="display:block">Błąd: Nieprawidłowe dane</div>';
            }

            document.getElementById('freeSpots').textContent = freeCount;
            document.getElementById('occupiedSpots').textContent = occupiedCount;
        }

        function updateLastUpdateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('pl-PL');
            document.getElementById('lastUpdate').textContent = timeString;
        }

        // Odświeżanie co 5 sekund
        setInterval(fetchParkingData, 5000);
        
        // Pierwsze pobranie
        fetchParkingData();
    </script>
