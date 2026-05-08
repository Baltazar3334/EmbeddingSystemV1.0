import requests


def load_workers_from_api(url: str):

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")

    data = response.json()

    workers = []

    print("\nLoading workers from API...")

    for person in data:

        keywords = person.get("keywords", [])
        bio = person.get("bio", "")

        if not keywords:
            continue

        workers.append({
            "id": person["id"],
            "name": f"{person['name']} {person['surname']}",
            "keywords": list(set(keywords)),
            "bio": bio
        })

    print(f"Loaded {len(workers)} workers")

    return workers