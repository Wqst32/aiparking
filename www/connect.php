<?php

$conn = new mysqli(
"mysql://root:mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD@mysql.railway.internal:3306/railway",
"root",
"mlUVabLxUQjJwkoBuADmrmtpaJcVEQMD",
"parking"
);

if ($conn->connect_error) {
die("blad");
}


?>

