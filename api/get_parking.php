<?php
header('Content-Type: application/json');

// Pobranie danych z environment variables Railway
$host = getenv('MYSQLHOST');
$port = getenv('MYSQLPORT');
$user = getenv('MYSQLUSER');
$password = getenv('MYSQLPASSWORD');
$database = getenv('MYSQLDATABASE');

// Sprawdzenie czy zmienne istnieją
if (!$host || !$user || !$password || !$database) {
    echo json_encode([
        'error' => 'Brak zmiennych środowiskowych bazy danych',
        'debug' => [
            'host_set' => !empty($host),
            'port_set' => !empty($port),
            'user_set' => !empty($user),
            'password_set' => !empty($password),
            'database_set' => !empty($database)
        ]
    ]);
    exit;
}

// Połączenie z bazą
$conn = new mysqli($host, $user, $password, $database, $port);

if ($conn->connect_error) {
    echo json_encode(['error' => 'Błąd połączenia: ' . $conn->connect_error]);
    exit;
}

// Sprawdź czy tabela 'parking' istnieje
$result = $conn->query("SHOW TABLES LIKE 'parking'");

if ($result->num_rows == 0) {
    // Utwórz tabelę parking
    $create_sql = "CREATE TABLE parking (
        id INT PRIMARY KEY,
        blacha VARCHAR(50) NOT NULL,
        status ENUM('wolne', 'zajete') DEFAULT 'wolne',
        czas TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )";
    
    if ($conn->query($create_sql)) {
        // Dodaj 6 miejsc parkingowych
        for ($i = 1; $i <= 6; $i++) {
            $conn->query("INSERT INTO parking (id, blacha, status) VALUES ($i, 'Miejsce $i', 'wolne')");
        }
    }
}

// Pobierz dane z parkingu
$sql = "SELECT id, blacha, status, 
        DATE_FORMAT(czas, '%H:%i:%s %d/%m/%Y') as czas 
        FROM parking 
        ORDER BY id";

$result = $conn->query($sql);
$parkingSpots = [];

if ($result) {
    while ($row = $result->fetch_assoc()) {
        $parkingSpots[] = $row;
    }
}

// Jeśli nie ma danych, zwróć puste miejsca
if (empty($parkingSpots)) {
    for ($i = 1; $i <= 6; $i++) {
        $parkingSpots[] = [
            'id' => $i,
            'blacha' => "Miejsce $i",
            'status' => 'wolne',
            'czas' => date('H:i:s d/m/Y')
        ];
    }
}

echo json_encode($parkingSpots);
$conn->close();
?>
