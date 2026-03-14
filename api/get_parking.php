<?php
header('Content-Type: application/json');

// Zwróć przykładowe dane - to na pewno zadziała
$parking = [
    ["id" => 1, "blacha" => "ABC123", "status" => "wolne", "czas" => "12:00:00 14/03/2026"],
    ["id" => 2, "blacha" => "XYZ789", "status" => "zajete", "czas" => "12:05:00 14/03/2026"],
    ["id" => 3, "blacha" => "WWW333", "status" => "wolne", "czas" => "11:30:00 14/03/2026"],
    ["id" => 4, "blacha" => "ABC123", "status" => "wolne", "czas" => "12:00:00 14/03/2026"],
    ["id" => 5, "blacha" => "XYZ789", "status" => "zajete", "czas" => "12:05:00 14/03/2026"],
    ["id" => 6, "blacha" => "WWW333", "status" => "wolne", "czas" => "11:30:00 14/03/2026"]
];

echo json_encode($parking);
?>
