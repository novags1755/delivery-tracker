# DashTrack v1.11
# Author: Gio
# Type: CLI delivery tracker
# Features: Logs delivery data, calculates earnings/tips, supports zone breakdowns, saves/loads CSV, filters by date

import os
import csv
from datetime import datetime

print("Welcome to DashTrack!")

# Global totals
total_miles = 0
total_earnings = 0
total_tips = 0
deliveries = []

#--- Functions ---
def log_zones():
    zones = []
    num_zones = int(input("How many zones do you want to log? "))
    for i in range(num_zones):
        zone = input(f"Enter zone #{i+1} name: ").strip()
        zones.append(zone)
    return zones

def log_delivery(zones):
    print("\nAvailable Zones:")
    for j, zone in enumerate(zones, 1):
        print(f"{j}. {zone}")
    zone_choice = int(input("Select zone number: "))
    zone_name = zones[zone_choice - 1]

    miles = float(input("Miles Driven: "))
    payment = float(input("Total payment ($): "))
    tip = float(input("Tip received ($): "))

    start_time = input("Enter start time (e.g., 6:45 AM): ")
    start_dt = datetime.strptime(start_time, "%I:%M %p")
    end_time = input("Enter end time (e.g., 7:05 AM): ")
    end_dt = datetime.strptime(end_time, "%I:%M %p")
    duration = end_dt - start_dt
    duration_minutes = duration.total_seconds() / 60

    notes = input("Any notes (merchant, special request, etc)? ")
    cost_per_mile = round(payment / miles, 2)

    return {
        "zone": zone_name,
        "miles": miles,
        "payment": payment,
        "tip": tip,
        "cpm": cost_per_mile,
        "start": start_time,
        "end": end_time,
        "duration": round(duration_minutes, 1),
        "notes": notes
    }

def log_multiple_deliveries(zones):
    global total_miles, total_earnings, total_tips
    num_deliveries = int(input("\nHow many deliveries do you want to log? "))
    for i in range(num_deliveries):
        print(f"\n--- Delivery #{i+1} ---")
        delivery = log_delivery(zones)
        deliveries.append(delivery)
        total_miles += delivery["miles"]
        total_earnings += delivery["payment"]
        total_tips += delivery["tip"]

def calculate_idle_time(deliveries):
    if len(deliveries) < 2:
        print("\nNot enough deliveries to calculate idle time")
        return
    
    total_idle = 0
    print("\n---Idle Time Between Deliveries---")
    for i in range(1,len(deliveries)):
        prev_end = datetime.strptime(deliveries[i-1]["end"], "%I:%M %p")
        curr_start = datetime.strptime(deliveries[i]["start"], "%I:%M %p")
        idle_minutes = (curr_start - prev_end).total_seconds() / 60

        if idle_minutes < 0:
            print(f"Warning: Overlapping times between delivery #{i} and #{i+1}")
            idle_minutes = 0

        total_idle += idle_minutes
        print(f"\nBetween delivery #{i} and #{i+1}: {round(idle_minutes, 1)} min")

        avg_idle = total_idle / (len(deliveries) - 1)
        print(f"\nTotal idle Time : {round(total_idle, 1)} minutes")
        print(f"\nAverage Idle Time: {round(avg_idle, 1)} minutes")


def print_summary(deliveries):  
    print("\n--- All Deliveries ---")
    for d in deliveries:
        print(f"""
Zone: {d['zone']}
Miles: {d['miles']}
Payment: ${d['payment']}
Tip: ${d['tip']}
Cost per Mile: ${d['cpm']}
Time: {d['start']} to {d['end']}
Duration: {d['duration']} minutes
Notes: {d['notes']}
------------------------------""")

def final_totals():
    print("\n=== Overall Summary ===")
    print(f"Total Deliveries Logged: {len(deliveries)}")
    print(f"Total Miles Driven: {total_miles}")
    print(f"Total Earnings: ${round(total_earnings, 2)}")
    print(f"Total Tips Earned: ${round(total_tips, 2)}")
    print(f"Average Earnings per Mile: ${round(total_earnings / total_miles, 2)}")

def zone_summary(deliveries):
    zone_data = {}
    for d in deliveries:
        zone = d["zone"]
        if zone not in zone_data:
            zone_data[zone] = {"count": 0, "earnings": 0, "miles": 0}
        zone_data[zone]["count"] += 1
        zone_data[zone]["earnings"] += d["payment"]
        zone_data[zone]["miles"] += d["miles"]

    print("\n=== Zone Breakdown ===")
    for zone, stats in zone_data.items():
        print(f"{zone}: {stats['count']} deliveries - ${round(stats['earnings'], 2)} earned - {round(stats['miles'], 1)} miles")

def save_deliveries_to_csv(deliveries, filename="deliveries_log.csv"):
    if not deliveries:
        print("No deliveries to save.")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"deliveries_{date_str}.csv"
    fieldnames = ["zone", "miles", "payment", "tip", "cpm", "start", "end", "duration", "notes"]
    file_exists = os.path.exists(filename)

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for delivery in deliveries:
                writer.writerow(delivery)
        print(f"\nDeliveries saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def load_deliveries_from_csv(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            loaded_deliveries = []
            for row in reader:
                delivery = {
                    "zone": row["zone"],
                    "miles": float(row["miles"]),
                    "payment": float(row["payment"]),
                    "tip": float(row["tip"]),
                    "cpm": float(row["cpm"]),
                    "start": row["start"],
                    "end": row["end"],
                    "duration": float(row["duration"]),
                    "notes": row["notes"]
                }
                loaded_deliveries.append(delivery)
            print(f"\nLoaded {len(loaded_deliveries)} deliveries from {filename}")
            return loaded_deliveries
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def filter_deliveries_by_date(deliveries):
    mode = input("\nFilter by single date or range? (single/range): ").strip().lower()

    if mode == "single":
        target_date = input("Enter the date (YYYY-MM-DD): ").strip()
        return [d for d in deliveries if target_date in d["start"]]

    elif mode == "range":
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        filtered = []
        for d in deliveries:
            delivery_date_str = d["start"].split()[0] if " " in d["start"] else d["start"]
            if start_date <= delivery_date_str <= end_date:
                filtered.append(d)
        return filtered

    else:
        print("Invalid option. Showing all deliveries.")
        return deliveries

def zone_performance_by_time(deliveries):
    if not deliveries:
        print("\nNo deliveries to analyze for zone/time performance.")
        return

    def get_time_period(start_str):
        dt = datetime.strptime(start_str, "%I:%M %p")
        hour = dt.hour
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 22:
            return "Evening"
        else:
            return "Late Night"

    performance = {}

    for d in deliveries:
        zone = d["zone"]
        time_period = get_time_period(d["start"])

        key = (zone, time_period)
        if key not in performance:
            performance[key] = {
                "count": 0,
                "earnings": 0,
                "miles": 0
            }
        performance[key]["count"] += 1
        performance[key]["earnings"] += d["payment"]
        performance[key]["miles"] += d["miles"]

    print("\n=== Zone Performance by Time of Day ===")
    for (zone, period), stats in performance.items():
        avg_payment = stats["earnings"] / stats["count"]
        print(f"{zone} | {period}: {stats['count']} deliveries - ${round(stats['earnings'], 2)} earned - "
              f"{round(stats['miles'], 1)} miles - Avg ${round(avg_payment, 2)} per delivery")

    
#--- Main Flow ---
zones = log_zones()
log_multiple_deliveries(zones)
print_summary(deliveries)
final_totals()
zone_summary(deliveries)
zone_performance_by_time(deliveries)
load_file = input("\nLoad a previous file to review? (y/n): ").strip().lower()
if load_file == "y":
    filename = input("Enter the filename (ex: deliveries_2025-04-11.csv): ").strip()
    previous_deliveries = load_deliveries_from_csv(filename)
    if previous_deliveries:
        use_filter = input("Filter deliveries by date? (y/n): ").strip().lower()
        if use_filter == "y":
            filtered = filter_deliveries_by_date(previous_deliveries)
            if filtered:
                print_summary(filtered)
                zone_summary(filtered)
                calculate_idle_time(filtered)
                zone_performance_by_time(filtered)

            else:
                print("No deliveries found for that date or range.")
        else:
            print_summary(previous_deliveries)
            zone_summary(previous_deliveries)
            calculate_idle_time(previous_deliveries)
            zone_performance_by_time(previous_deliveries)

calculate_idle_time(deliveries)
save_deliveries_to_csv(deliveries)

# Reset totals
total_miles = 0
total_earnings = 0
total_tips = 0