from api import get_trains_between_stations, get_train_schedule
from mock_data import get_mock_availability, get_delay_info

# nearby stations graph - manually built for common origins
# TODO: make dynamic using station search API
NEARBY_STATIONS = {
    "NDLS": ["NZM", "DLI", "DEE", "ANVT"],
    "PNBE": ["RJPB", "DNR"],
    "RNC":  ["HZD", "BKSC"],
    "BCT":  ["BVI", "ADH"],
    "MAS":  ["MSB", "TBM"],
}


def estimate_confirmation_chance(availability_str):
    if not availability_str or availability_str == "N/A":
        return "unknown", 0

    avail = availability_str.upper()

    if "AVL" in avail:
        try:
            seats = int(''.join(filter(str.isdigit, avail)))
            if seats > 20:
                return "high", seats
            elif seats > 5:
                return "medium", seats
            else:
                return "low", seats
        except:
            return "high", 0

    elif "WL" in avail:
        try:
            wl_number = int(''.join(filter(str.isdigit, avail)))
            if wl_number <= 5:
                return "likely to confirm", wl_number
            elif wl_number <= 15:
                return "might confirm", wl_number
            elif wl_number <= 30:
                return "risky", wl_number
            else:
                return "unlikely", wl_number
        except:
            return "waitlisted", 0

    elif "RAC" in avail:
        return "RAC - partial confirm", 0

    elif "REGRET" in avail:
        return "no seats", 0

    return "unknown", 0


def search_direct_trains(from_station, to_station, date, travel_class):
    print(f"\n  searching direct trains: {from_station} -> {to_station}")
    result = get_trains_between_stations(from_station, to_station, date)

    if not result or not result.get("data"):
        print("  no trains found")
        return []

    trains = result["data"]
    train_results = []

    for train in trains:
        train_no = train.get("train_number")
        train_name = train.get("train_name", "Unknown")
        departure = train.get("from_std", "??:??")
        arrival = train.get("to_std", "??:??")
        duration = train.get("duration", "N/A")
        run_days = train.get("run_days", [])
        has_pantry = train.get("has_pantry", False)

        # get availability from mock data
        availability = get_mock_availability(train_no, from_station, to_station, travel_class)
        chance, wl_num = estimate_confirmation_chance(availability)

        # get delay info for this train
        delay_info = get_delay_info(train_no)

        train_results.append({
            "train_no": train_no,
            "train_name": train_name,
            "from": from_station,
            "to": to_station,
            "departure": departure,
            "arrival": arrival,
            "duration": duration,
            "run_days": run_days,
            "has_pantry": has_pantry,
            "availability": availability,
            "chance": chance,
            "wl_num": wl_num,
            "avg_delay": delay_info["avg_delay_mins"],
            "reliability": delay_info["reliability"],
            "type": "direct"
        })

    # sort: available first, then by waitlist number, then by delay
    train_results.sort(key=lambda x: (
        0 if "high" in x["chance"] or "medium" in x["chance"] else
        1 if "likely" in x["chance"] or "RAC" in x["chance"] else
        2 if "might" in x["chance"] else
        3,
        x["wl_num"],
        x["avg_delay"]
    ))

    return train_results


def find_alternate_boarding_points(train_no, original_from, to_station, date, travel_class):
    print(f"\n  checking alternate boarding points for train {train_no}...")

    schedule_data = get_train_schedule(train_no)
    if not schedule_data or not schedule_data.get("data"):
        return []

    stations = schedule_data["data"]
    alternates = []

    our_position = None
    for i, station in enumerate(stations):
        code = station.get("station_code", "")
        if code == original_from:
            our_position = i
            break

    if our_position is None:
        return []

    # check 3 stations before our boarding point
    for i in range(max(0, our_position - 3), our_position):
        alt_station = stations[i]
        alt_code = alt_station.get("station_code", "")
        alt_name = alt_station.get("station_name", alt_code)

        if not alt_code:
            continue

        availability = get_mock_availability(train_no, alt_code, to_station, travel_class)
        # earlier stations sometimes have better availability due to origin quota
        # simulate slight improvement for demo
        if availability and "WL" in availability:
            try:
                wl_num = int(''.join(filter(str.isdigit, availability)))
                improved_wl = max(1, wl_num - 5)  # earlier station quota is slightly better
                availability = f"WL {improved_wl}"
            except:
                pass

        chance, wl_num = estimate_confirmation_chance(availability)

        alternates.append({
            "station_code": alt_code,
            "station_name": alt_name,
            "availability": availability,
            "chance": chance,
            "wl_num": wl_num,
            "note": f"board here, set {original_from} as boarding point on IRCTC"
        })

    return alternates


def search_nearby_origin_trains(from_station, to_station, date, travel_class):
    nearby = NEARBY_STATIONS.get(from_station, [])
    if not nearby:
        print(f"\n  no nearby stations configured for {from_station}")
        return []

    print(f"\n  checking nearby stations: {nearby}")
    all_results = []
    seen_trains = set()  # avoid showing same train twice

    for alt_station in nearby:
        result = get_trains_between_stations(alt_station, to_station, date)
        if not result or not result.get("data"):
            continue

        for train in result["data"]:
            train_no = train.get("train_number")

            # skip if already shown in direct results
            if train_no in seen_trains:
                continue
            seen_trains.add(train_no)

            train_name = train.get("train_name", "Unknown")
            departure = train.get("from_std", "??:??")
            duration = train.get("duration", "N/A")
            run_days = train.get("run_days", [])
            has_pantry = train.get("has_pantry", False)

            availability = get_mock_availability(train_no, alt_station, to_station, travel_class)
            chance, wl_num = estimate_confirmation_chance(availability)
            delay_info = get_delay_info(train_no)

            all_results.append({
                "train_no": train_no,
                "train_name": train_name,
                "from": alt_station,
                "to": to_station,
                "departure": departure,
                "duration": duration,
                "run_days": run_days,
                "availability": availability,
                "chance": chance,
                "wl_num": wl_num,
                "avg_delay": delay_info["avg_delay_mins"],
                "reliability": delay_info["reliability"],
                "type": "nearby_origin",
                "has_pantry": has_pantry
            })

    all_results.sort(key=lambda x: (
        0 if "high" in x["chance"] or "medium" in x["chance"] else
        1 if "likely" in x["chance"] or "RAC" in x["chance"] else
        2,
        x["wl_num"],
        x["avg_delay"]
    ))

    return all_results
