import requests
import time

url = "https://datasets-server.huggingface.co/rows"
params = {
    "dataset": "lamini/earnings-calls-qa",
    "config": "default",
    "split": "train",
    "offset": 0,
    "length": 100
}

all_rows = []
offset = 0
batch_size = 100

while True:
    params["offset"] = offset
    print(f"Fetching rows {offset}-{offset + batch_size}...")

    response = requests.get(url, params=params)

    try:
        data = response.json()
    except ValueError:
        print("❌ No valid JSON returned. Possibly reached end of dataset.")
        break

    rows = [row["row"] for row in data.get("rows", [])]
    if not rows:
        print("✅ No more rows. Done.")
        break

    all_rows.extend(rows)
    offset += batch_size
    time.sleep(1)
