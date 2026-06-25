from colorama import Fore, Style, init

init(autoreset=True)


def print_header():
    print(Fore.CYAN + "=" * 62)
    print(Fore.CYAN + "       SMART TRAIN ROUTE ADVISOR")
    print(Fore.CYAN + "       Finds best options when IRCTC tickets are hard to get")
    print(Fore.CYAN + "=" * 62)


def get_chance_color(chance):
    chance = chance.lower()
    if "high" in chance or "medium" in chance:
        return Fore.GREEN
    elif "likely" in chance or "rac" in chance or "low" in chance:
        return Fore.YELLOW
    elif "might" in chance:
        return Fore.YELLOW
    elif "risky" in chance or "unlikely" in chance or "no seats" in chance:
        return Fore.RED
    return Fore.WHITE


def get_reliability_color(reliability):
    if reliability == "good":
        return Fore.GREEN
    elif reliability == "moderate":
        return Fore.YELLOW
    elif reliability == "poor":
        return Fore.RED
    return Fore.WHITE


def print_train_result(train, index):
    chance_color = get_chance_color(train["chance"])
    rel_color = get_reliability_color(train.get("reliability", "unknown"))

    run_days = ", ".join(train.get("run_days", [])) or "Daily"
    pantry = "Yes" if train.get("has_pantry") else "No"
    delay = train.get("avg_delay", 0)
    reliability = train.get("reliability", "unknown")

    print(f"\n  {index}. {Fore.WHITE}{train['train_no']} - {train['train_name']}")
    print(f"     Route       : {train['from']} -> {train['to']}")
    print(f"     Departure   : {train.get('departure', 'N/A')}  |  Duration: {train.get('duration', 'N/A')}")
    print(f"     Runs on     : {run_days}")
    print(f"     Pantry      : {pantry}")
    print(f"     Availability: {chance_color}{train['availability']}")
    print(f"     Chance      : {chance_color}{train['chance'].upper()}")
    print(f"     Avg Delay   : {rel_color}{delay} mins  ({reliability} reliability)")

    if train.get("type") == "nearby_origin":
        print(f"     {Fore.CYAN}[Tip] Board from {train['from']} - check if this train stops at your original station too")


def print_alternate_boarding(alternates, train_no, train_name):
    if not alternates:
        print(f"  no alternate boarding data available for train {train_no}")
        return

    print(Fore.CYAN + f"\n  Alternate Boarding Points for {train_no} - {train_name}")
    print(f"  {Fore.WHITE}(board from an earlier station using IRCTC boarding point change)")

    for alt in alternates:
        color = get_chance_color(alt["chance"])
        print(f"\n    {alt['station_name']} ({alt['station_code']})")
        print(f"    Availability : {color}{alt['availability']}")
        print(f"    Chance       : {color}{alt['chance'].upper()}")
        print(f"    How          : {alt['note']}")


def print_section(title):
    print(f"\n{Fore.CYAN}{'=' * 62}")
    print(f"{Fore.CYAN}  {title}")
    print(f"{Fore.CYAN}{'=' * 62}")


def print_waitlist_tips(trains):
    waitlisted = [t for t in trains if t.get("availability") and "WL" in t["availability"]]
    if not waitlisted:
        return

    print(f"\n{Fore.YELLOW}  WAITLIST INSIGHTS:")
    print(f"  WL < 5   : Almost always confirms before journey")
    print(f"  WL 5-15  : Good chance of confirming, monitor closely")
    print(f"  WL 15-30 : Risky, consider tatkal 1 day before")
    print(f"  WL > 30  : Book alternate or premium tatkal")
    print(f"\n  GENERAL TIPS:")
    print(f"  - Check availability again 4-5 days before journey (cancellations peak)")
    print(f"  - Try RLWL quota - clears independently from main WL")
    print(f"  - Rajdhani 3A often clears faster than 2A on this route")
    print(f"  - Tatkal opens at 10am, 1 day before journey for most trains")
