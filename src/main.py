from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

TOKEN = os.getenv("DISCOGS_TOKEN")
USERNAME = os.getenv("USERNAME")

HEADERS = {
    "Authorization": f"Discogs token={TOKEN}",
    "User-Agent": "discogs-agent/1.0"
}

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, "data", "prices.json")


def get_wantlist():
    url = f"https://api.discogs.com/users/{USERNAME}/wants"
    res = requests.get(url, headers=HEADERS)
    data = res.json()
    return data["wants"]


def get_price(release_id):
    url = f"https://api.discogs.com/marketplace/stats/{release_id}"
    res = requests.get(url, headers=HEADERS)
    data = res.json()
    return data.get("lowest_price")


if __name__ == "__main__":
    wants = get_wantlist()

    results = []

    for item in wants[:5]:
        title = item["basic_information"]["title"]
        release_id = item["id"]

        price = get_price(release_id)

        print(title, price)

        results.append({
            "title": title,
            "price": price
        })

    # salvar dados
with open(file_path, "w") as f:
    json.dump(results, f, indent=2)

    print("\n✅ Dados salvos em data/prices.json")