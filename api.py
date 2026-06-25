import requests
import json
import os

# put your rapidapi key here
API_KEY = "YOUR_RAPIDAPI_KEY_HERE"

BASE_URL = "https://irctc1.p.rapidapi.com/api/v3"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "irctc1.p.rapidapi.com"
}

# cache folder to save API responses so we don't waste requests
CACHE_FOLDER = "cache"
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)


def get_from_cache(filename):
    path = os.path.join(CACHE_FOLDER, filename)
    if os.path.exists(path):
        print(f"  [cache] loading {filename} from cache...")
        with open(path, "r") as f:
            return json.load(f)
    return None


def save_to_cache(filename, data):
    path = os.path.join(CACHE_FOLDER, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  [cache] saved {filename}")


def get_trains_between_stations(from_station, to_station, date):
    # date format: YYYYMMDD  eg. 20260810
    cache_file = f"trains_{from_station}_{to_station}_{date}.json"

    cached = get_from_cache(cache_file)
    if cached:
        return cached

    print(f"  [api] fetching trains from {from_station} to {to_station}...")
    url = f"{BASE_URL}/trainBetweenStations"
    params = {
        "fromStationCode": from_station,
        "toStationCode": to_station,
        "dateOfJourney": date
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        save_to_cache(cache_file, data)
        return data
    except Exception as e:
        print(f"  [error] could not fetch trains: {e}")
        return None


def check_seat_availability(train_no, from_station, to_station, date, class_type, quota="GN"):
    cache_file = f"seats_{train_no}_{from_station}_{to_station}_{date}_{class_type}.json"

    cached = get_from_cache(cache_file)
    if cached:
        return cached

    print(f"  [api] checking seats for train {train_no} class {class_type}...")
    url = f"{BASE_URL}/checkSeatAvailability"
    params = {
        "classType": class_type,
        "fromStationCode": from_station,
        "quota": quota,
        "toStationCode": to_station,
        "trainNo": train_no,
        "date": date
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        save_to_cache(cache_file, data)
        return data
    except Exception as e:
        print(f"  [error] could not check seats: {e}")
        return None


def get_train_schedule(train_no):
    cache_file = f"schedule_{train_no}.json"

    cached = get_from_cache(cache_file)
    if cached:
        return cached

    print(f"  [api] fetching schedule for train {train_no}...")
    url = f"{BASE_URL}/getTrainSchedule"  
    params = {"trainNo": train_no}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        save_to_cache(cache_file, data)
        return data
    except Exception as e:
        print(f"  [error] could not fetch schedule: {e}")
        return None
