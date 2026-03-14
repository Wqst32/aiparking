<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

// Konfiguracja bazy danych - Railway ustawia zmienne środowiskowe
$host = getenv('MYSQLHOST') ?: 'localhost';
$port = getenv('MYSQLPORT') ?: '3306';
$user = getenv('MYSQLUSER') ?: 'root';
$password = getenv('MYSQLPASSWORD') ?: '';
$database = getenv('MYSQLDATABASE') ?: 'railway';

// Połączenie z bazą danych
$conn = new mysqli($host, $user, $password, $database, $port);

if ($conn->connect_error) {
    die(json_encode(['error' => 'Błąd połączenia: ' . $conn->connect_error]));
}

// Zapytanie - zakładam że Twoja tabela nazywa się 'parking'
// Jeśli nazywa się inaczej, zmień 'parking' na właściwą nazwę
$sql = "SELECT id, blacha, status, 
        DATE_FORMAT(czas, '%H:%i:%s %d/%m/%Y') as czas 
        FROM parking 
        ORDER BY id";

$result = $conn->query($sql);

$parkingSpots = [];
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $parkingSpots[] = $row;
    }
}

echo json_encode($parkingSpots);
$conn->close();
?>
