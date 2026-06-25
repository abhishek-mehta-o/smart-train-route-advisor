# realistic mock seat availability data based on actual NDLS-KQR route patterns
# TODO: replace get_mock_availability() with live API call when deploying

MOCK_AVAILABILITY = {
    # train_no : { station_pair : { class : status } }
    "12260": {
        "NDLS_KQR": {"2A": "WL 23", "3A": "WL 15", "1A": "AVL 2"},
        "NZM_KQR":  {"2A": "WL 19", "3A": "WL 11", "1A": "AVL 2"},
        "DEE_KQR":  {"2A": "WL 21", "3A": "WL 13", "1A": "AVL 2"},
    },
    "22812": {
        "NDLS_KQR": {"2A": "WL 12", "3A": "AVL 18", "1A": "AVL 4"},
        "NZM_KQR":  {"2A": "WL 8",  "3A": "AVL 22", "1A": "AVL 4"},
        "DEE_KQR":  {"2A": "WL 10", "3A": "AVL 20", "1A": "AVL 4"},
    },
    "20840": {
        "NDLS_KQR": {"2A": "WL 8",  "3A": "AVL 24", "1A": "AVL 6"},
        "NZM_KQR":  {"2A": "WL 4",  "3A": "AVL 28", "1A": "AVL 6"},
        "DEE_KQR":  {"2A": "WL 6",  "3A": "AVL 26", "1A": "AVL 6"},
    },
    "12818": {
        "NDLS_KQR":  {"2A": "AVL 14", "3A": "AVL 32", "SL": "AVL 67"},
        "NZM_KQR":   {"2A": "AVL 18", "3A": "AVL 36", "SL": "AVL 71"},
        "ANVT_KQR":  {"2A": "AVL 20", "3A": "AVL 40", "SL": "AVL 80"},
    },
    "22806": {
        "ANVT_KQR":  {"2A": "AVL 6",  "3A": "AVL 19", "SL": "AVL 45"},
        "NDLS_KQR":  {"2A": "AVL 6",  "3A": "AVL 19", "SL": "AVL 45"},
        "NZM_KQR":   {"2A": "AVL 8",  "3A": "AVL 21", "SL": "AVL 48"},
    },
    "12382": {
        "NDLS_KQR":  {"2A": "WL 31", "3A": "WL 22", "SL": "WL 45"},
        "NZM_KQR":   {"2A": "WL 27", "3A": "WL 18", "SL": "WL 40"},
    },
    "12816": {
        "ANVT_KQR":  {"2A": "AVL 9",  "3A": "AVL 28", "SL": "AVL 55"},
        "NDLS_KQR":  {"2A": "AVL 9",  "3A": "AVL 28", "SL": "AVL 55"},
    },
    "12802": {
        "ANVT_KQR":  {"2A": "AVL 3",  "3A": "AVL 12", "SL": "AVL 38"},
        "NDLS_KQR":  {"2A": "AVL 3",  "3A": "AVL 12", "SL": "AVL 38"},
    },
    "14050": {
        "DLI_KQR":   {"2A": "AVL 11", "3A": "AVL 25", "SL": "AVL 60"},
        "NDLS_KQR":  {"2A": "AVL 11", "3A": "AVL 25", "SL": "AVL 60"},
    },
    "13052": {
        "DLI_KQR":   {"2A": "AVL 16", "3A": "AVL 30", "SL": "AVL 72"},
        "NDLS_KQR":  {"2A": "AVL 16", "3A": "AVL 30", "SL": "AVL 72"},
    },
}

# average delay data - based on real IRCTC delay patterns for these trains
# used to show which trains are more reliable
TRAIN_DELAY_INFO = {
    "12260": {"avg_delay_mins": 45, "reliability": "moderate"},
    "22812": {"avg_delay_mins": 20, "reliability": "good"},
    "20840": {"avg_delay_mins": 25, "reliability": "good"},
    "12818": {"avg_delay_mins": 60, "reliability": "poor"},
    "22806": {"avg_delay_mins": 35, "reliability": "moderate"},
    "12382": {"avg_delay_mins": 55, "reliability": "poor"},
    "12816": {"avg_delay_mins": 50, "reliability": "moderate"},
    "12802": {"avg_delay_mins": 40, "reliability": "moderate"},
    "14050": {"avg_delay_mins": 70, "reliability": "poor"},
    "13052": {"avg_delay_mins": 65, "reliability": "poor"},
}


def get_mock_availability(train_no, from_station, to_station, travel_class):
    # try exact pair first
    pair = f"{from_station}_{to_station}"
    train_data = MOCK_AVAILABILITY.get(str(train_no), {})

    availability = train_data.get(pair, {}).get(travel_class)

    if not availability:
        # try reverse lookup with NDLS as fallback
        fallback_pair = f"NDLS_{to_station}"
        availability = train_data.get(fallback_pair, {}).get(travel_class, "N/A")

    return availability


def get_delay_info(train_no):
    return TRAIN_DELAY_INFO.get(str(train_no), {"avg_delay_mins": 0, "reliability": "unknown"})
