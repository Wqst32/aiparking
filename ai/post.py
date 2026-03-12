import requests

url = "https://github.com/Wqst32/aiparking/blob/main/www/save.php"

params = {
"id": 2,
"blacha": "PO12345",
"status": "zajete"
}

requests.get(url, params=params)