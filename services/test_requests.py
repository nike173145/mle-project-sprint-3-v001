import time
import math
import random
import requests


URL = "http://localhost:1703/predict"

COLUMNS = [
    "building_id",
    "floor",
    "kitchen_area",
    "rooms",
    "total_area",
    "latitude",
    "longitude",
    "ceiling_height",
    "floors_total",
    "1/floor",
    "exp(rooms)",
    "1/building_id",
    "1/floors_total",
    "flats_count**3",
    "building_type_int**3",
    "has_elevator",
    "floor**3",
    "1/flats_count",
]


def generate_random_object():
    """Генерирует один случайный объект недвижимости."""

    building_id = random.randint(1000, 30000)

    floors_total = random.randint(5, 25)
    floor = random.randint(1, floors_total)

    rooms = random.randint(1, 5)
    kitchen_area = round(random.uniform(5, 20), 2)
    total_area = round(random.uniform(30, 120), 2)

    latitude = round(random.uniform(55.55, 56.05), 6)
    longitude = round(random.uniform(37.20, 37.95), 6)

    ceiling_height = round(random.uniform(2.5, 3.2), 2)

    flats_count = random.randint(50, 500)
    building_type_int = random.choice([1, 2, 3, 4])
    has_elevator = random.choice([0, 1])

    row = [
        building_id,
        floor,
        kitchen_area,
        rooms,
        total_area,
        latitude,
        longitude,
        ceiling_height,
        floors_total,
        1 / floor,
        math.exp(rooms),
        1 / building_id,
        1 / floors_total,
        flats_count ** 3,
        building_type_int ** 3,
        has_elevator,
        floor ** 3,
        1 / flats_count,
    ]

    return row


for i in range(40):
    payload = {
        "user_id": i,
        "model_params": {
            "columns": COLUMNS,
            "data": [
                generate_random_object()
            ],
        },
    }

    response = requests.post(URL, json=payload)

    print(f"Request #{i}")
    print("Status code:", response.status_code)

    try:
        print("Response:", response.json())
    except Exception:
        print("Raw response:", response.text)

    print("-" * 50)

    if i == 30:
        time.sleep(30)

    time.sleep(2)