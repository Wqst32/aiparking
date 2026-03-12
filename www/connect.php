<?php

$conn = new mysqli(
"mysql://root:mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD@caboose.proxy.rlwy.net:47538/railway",
"root",
"mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD",
"parking"
);

if ($conn->connect_error) {
die("blad");
}


?>
