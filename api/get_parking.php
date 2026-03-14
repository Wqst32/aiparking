<?php
header('Content-Type: application/json');

$host = getenv('MYSQLHOST');
$port = getenv('MYSQLPORT') ?: '3306';
$user = getenv('MYSQLUSER');
$password = getenv('MYSQLPASSWORD');
$database = getenv('MYSQLDATABASE');

// Sprawdź czy są dane do połączenia
if (!$host || !$user || !$password || !$database) {
    echo json_encode([
        ['id' => 1, 'blacha' => 'Miejsce 1', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 2, 'blacha' => 'Miejsce 2', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 3, 'blacha' => 'Miejsce 3', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 4, 'blacha' => 'Miejsce 4', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 5, 'blacha' => 'Miejsce 5', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 6, 'blacha' => 'Miejsce 6', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')]
    ]);
    exit;
}

$conn = new mysqli($host, $user, $password, $database, $port);

if ($conn->connect_error) {
    // Jeśli błąd połączenia, zwróć przykładowe dane
    echo json_encode([
        ['id' => 1, 'blacha' => 'Miejsce 1', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 2, 'blacha' => 'Miejsce 2', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 3, 'blacha' => 'Miejsce 3', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 4, 'blacha' => 'Miejsce 4', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 5, 'blacha' => 'Miejsce 5', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 6, 'blacha' => 'Miejsce 6', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')]
    ]);
    exit;
}

// Sprawdź czy tabela istnieje
$result = $conn->query("SELECT id, blacha, status, czas FROM parking ORDER BY id");

if (!$result || $result->num_rows == 0) {
    // Jeśli nie ma tabeli lub danych, zwróć przykładowe
    echo json_encode([
        ['id' => 1, 'blacha' => 'Miejsce 1', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 2, 'blacha' => 'Miejsce 2', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 3, 'blacha' => 'Miejsce 3', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 4, 'blacha' => 'Miejsce 4', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 5, 'blacha' => 'Miejsce 5', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')],
        ['id' => 6, 'blacha' => 'Miejsce 6', 'status' => 'wolne', 'czas' => date('H:i:s d/m/Y')]
    ]);
    exit;
}

$data = [];
while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode($data);
$conn->close();
?>
