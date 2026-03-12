<?php

include "connect.php";

$id = $_GET["id"];
$blacha = $_GET["blacha"];
$status = $_GET["status"];

$sql = "UPDATE parking 
SET blacha='$blacha', status='$status'
WHERE id=$id";

$conn->query($sql);

echo "ok";

?>