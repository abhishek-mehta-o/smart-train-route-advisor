from search import search_direct_trains, find_alternate_boarding_points, search_nearby_origin_trains
from display import (print_header, print_train_result, print_alternate_boarding,
                     print_section, print_waitlist_tips)

VALID_CLASSES = ["SL", "2A", "3A", "1A", "CC", "EC", "2S"]


def get_user_input():
    print("\n  Enter journey details:")
    from_station = input("  From Station Code (eg. NDLS) : ").strip().upper()
    to_station   = input("  To Station Code   (eg. KQR)  : ").strip().upper()
    date         = input("  Date (YYYYMMDD)   (eg. 20260810): ").strip()

    print(f"\n  Classes: {', '.join(VALID_CLASSES)}")
    travel_class = input("  Travel Class (eg. 2A): ").strip().upper()

    if travel_class not in VALID_CLASSES:
        print("  invalid class, defaulting to SL")
        travel_class = "SL"

    return from_station, to_station, date, travel_class


def main():
    print_header()
    from_station, to_station, date, travel_class = get_user_input()

    print(f"\n  Route : {from_station} -> {to_station} | {date} | Class: {travel_class}")
    print("  (first run fetches live data, subsequent runs use cache)\n")

    # step 1: direct trains
    print_section("DIRECT TRAINS")
    direct_trains = search_direct_trains(from_station, to_station, date, travel_class)

    if not direct_trains:
        print("  no direct trains found")
    else:
        for i, train in enumerate(direct_trains[:8]):
            print_train_result(train, i + 1)

    # step 2: alternate boarding points for waitlisted trains
    waitlisted = [t for t in direct_trains if t.get("availability") and "WL" in t["availability"]]
    if waitlisted:
        print_section("ALTERNATE BOARDING POINTS")
        print("  Same train, board from an earlier station for better quota availability")
        for train in waitlisted[:2]:
            alternates = find_alternate_boarding_points(
                train["train_no"], from_station, to_station, date, travel_class
            )
            print_alternate_boarding(alternates, train["train_no"], train["train_name"])

    # step 3: nearby origin stations
    print_section("TRAINS FROM NEARBY STATIONS")
    print("  Explore trains from stations near your origin")
    nearby_trains = search_nearby_origin_trains(from_station, to_station, date, travel_class)

    if not nearby_trains:
        print("  no nearby station options found")
    else:
        for i, train in enumerate(nearby_trains[:4]):
            print_train_result(train, i + 1)

    # step 4: waitlist tips
    print_section("WAITLIST INSIGHTS & TIPS")
    print_waitlist_tips(direct_trains + nearby_trains)

    print("\n" + "=" * 62)
    print("  search complete. results cached for instant re-runs.")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()
