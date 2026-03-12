<?php

$conn = new mysqli(
"mysql-aiparking.alwaysdata.net",
"aiparking",
"zaq1@WSX",
"aiparking_parking"
);

if ($conn->connect_error) {
die("blad");
}

?>