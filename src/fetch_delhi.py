import requests
import json
import os

RAW_DATA_PATH = os.path.join("data", "raw", "delhi_raw.json")

URL = "https://www.swiggy.com/dapi/restaurants/list/v5"

params = {
    "lat": 28.6139,
    "lng": 77.2090,
    "page_type": "DESKTOP_WEB_LISTING"
}

# ★ Important: Add browser headers to avoid 403
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.82 Safari/537.36",
    "Accept": "application/json",
}

response = requests.get(URL, params=params, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Delhi restaurant data saved to delhi_raw.json")
else:
    print("Error:", response.status_code)
    print(response.text[:500])  # show first part of error
