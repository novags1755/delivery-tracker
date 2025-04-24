# DashTrack v1.12
# Author: Gio
# Type: CLI delivery tracker
# Features: Logs delivery data, calculates earnings/tips, supports zone breakdowns, saves/loads CSV, filters by date

import os
import csv
import sqlite3
DB_NAME = "dashtrack.db"
from datetime import datetime

print("Welcome to DashTrack!")


def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #Creates zones table

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS zones (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE NOT NULL
            );
        """)
    #Creates Deliveries table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   zone_id INTEGER NOT NULL,
                   miles REAL NOT NULL,
                   payment REAL NOT NULL,
                   tip REAL NOT NULL,
                   cpm REAL NOT NULL,
                   start_time TEXT NOT NULL,
                   end_time TEXT NOT NULL,
                   duration REAL NOT NULL,
                   notes TEXT,
                   FOREIGN KEY (zone_id) REFERENCES zones (id)
            );
        """)
    

    conn.commit()
    conn.close()
initialize_database()

# Global totals
total_miles = 0
total_earnings = 0
total_tips = 0
deliveries = []

#--- Functions ---
def log_zones():
    zones = []
    while True:
        try:
            num_zones = int(input("How many zones do you want to log? "))
            if num_zones < 1:
                print("Please enter at least one zone.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    for i in range(num_zones):
        zone = input(f"Enter zone #{i+1} name: ").strip()
        zones.append(zone)
    return zones


def get_idle_time(prev_end, curr_start):
    prev_end_dt = datetime.strptime(prev_end, "%I:%M %p")
    curr_start_dt = datetime.strptime(curr_start, "%I:%M %p")
    idle_minutes = (curr_start_dt - prev_end_dt).total_seconds() / 60
    return max(0, idle_minutes, 0)

def calculate_idle_time(deliveries):
    if len(deliveries) < 2:
        print("\nNot enough deliveries to calculate idle time")
        return
    
    total_idle = 0
    print("\n---Idle Time Between Deliveries---")

    for i in range(1, len(deliveries)):
        idle_minutes = get_idle_time(deliveries[i-1]["end"], deliveries[i]["start"])

        if idle_minutes == 0:
            print(f"Warning: Overlapping times between delivery #{i} and #{i+1}")

        total_idle += idle_minutes
        print(f"\nBetween delivery #{i} and #{i+1}: {round(idle_minutes, 1)} minutes")

    avg_idle = total_idle / (len(deliveries) - 1)
    print(f"\nTotal idle Time : {round(total_idle, 1)} minutes")
    print(f"\nAverage Idle Time: {round(avg_idle, 1)} minutes")

def get_zone_choice(zones):
    print("\nAvailable Zones:")
    for j, zone in enumerate(zones, 1):
        print(f"{j}. {zone}")
    
    while True:
        try:
            zone_choice = int(input("Select zone number: "))
            if 1 <= zone_choice <= len(zones):
                return zones[zone_choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(zones)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_delivery_input_fields():
    while True:
        try:
            miles = float(input("Miles Driven: "))
            payment = float(input("Total payment ($): "))
            tip = float(input("Tip received ($): "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    while True:
        try:
            start_time = input("Enter start time (e.g., 6:45 AM): ")
            start_dt = datetime.strptime(start_time, "%I:%M %p")
            end_time = input("Enter end time (e.g., 7:05 AM): ")
            end_dt = datetime.strptime(end_time, "%I:%M %p")
            if end_dt <= start_dt:
                print("End time must be after start time.")
                continue
            break
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM format.")
    
    duration_minutes = (end_dt - start_dt).total_seconds() / 60
    notes = input("Any notes (merchant, special request, etc)? ")

    return miles, payment, tip, start_time, end_time, duration_minutes, notes


def build_delivery_entry(zone,miles, payment, tip, start_time, end_time, duration_minutes, notes):
    cost_per_mile = round(payment / miles, 2)
    return {
        "zone": zone,
        "miles": miles,
        "payment": payment,
        "tip": tip,
        "cpm": cost_per_mile,
        "start": start_time,
        "end": end_time,
        "duration": round(duration_minutes, 1),
        "notes": notes
    }

def log_delivery(zones):
    zone_name = get_zone_choice(zones)
    miles, payment, tip, start_time, end_time, duration_minutes, notes = get_delivery_input_fields()
    delivery = build_delivery_entry(zone_name, miles, payment, tip, start_time, end_time, duration_minutes, notes)
    return delivery

def log_multiple_deliveries(zones):
    global total_miles, total_earnings, total_tips

    while True:
        try:
            num_deliveries = int(input("\nHow many deliveries do you want to log? "))
            if num_deliveries < 1:
                print("Enter at least one delivery.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for i in range(num_deliveries):
        print(f"\n--- Delivery #{i+1} ---")
        delivery = log_delivery(zones)
        deliveries.append(delivery)
        total_miles += delivery["miles"]
        total_earnings += delivery["payment"]
        total_tips += delivery["tip"]


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

def get_zone_stats(deliveries):
    zone_data = {}
    for d in deliveries:
        zone = d["zone"]
        if zone not in zone_data:
            zone_data[zone] = {"count": 0, "earnings": 0, "miles": 0}
        zone_data[zone]["count"] += 1
        zone_data[zone]["earnings"] += d["payment"]
        zone_data[zone]["miles"] += d["miles"]
    return zone_data

def zone_summary(deliveries):
    zone_data = get_zone_stats(deliveries)
    print("\n=== Zone Breakdown ===")
    for zone, stats in zone_data.items():
        print(f"{zone}: {stats['count']} deliveries - ${round(stats['earnings'], 2)} "
              f"earned - {round(stats['miles'], 1)} miles"
                )

def save_deliveries_to_db(deliveries):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for d in deliveries:
        #Ensure zone exists in the database or insert it
        cursor.execute("INSERT OR IGNORE INTO zones (name) VALUES (?)", (d["zone"],))
        cursor.execute("SELECT id FROM zones WHERE name = ?", (d["zone"],))
        zone_id = cursor.fetchone()[0]
        #insert the delivery
        cursor.execute("""
            INSERT INTO deliveries (zone_id, miles, payment, tip, cpm, start_time, end_time, duration, notes
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                                        zone_id, d["miles"], d["payment"], d["tip"], d["cpm"],
                                        d["start"], d["end"], d["duration"], d["notes"]
                                    ))
            
    conn.commit()
    conn.close()
    print(f"\nDeliver saved to database: {DB_NAME}")

def load_deliveries_from_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
        SELECT z.name, d.miles, d.payment, d.tip, d.cpm, d.start_time, d.end_time, d.duration, d.notes
        FROM deliveries d
        JOIN zones z ON d.zone_id = z.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    deliveries = []
    for rown in rows:
        delivery = {
            "zone": row[0],
            "miles": row[1],
            "payment": row[2],
            "tip": row[3],
            "cpm": row[4],
            "start": row[5],
            "end": row[6],
            "duration": row[7],
            "notes": row[8]
        }
        deliveries.append(delivery)
    
    print(f"\nLoaded {len(deliveries)} deliveries from database")
    return deliveries



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
    
def get_time_period(start_str):
    dt = datetime.strptime(start_str, "%I:%M %p")
    hour = dt.hour
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Late Night"
    
            
def zone_performance_by_time(deliveries):
    if not deliveries:
        print("\nNo deliveries to analyze for zone/time performance.")
        return
    
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
                  f"{round(stats['miles'], 1)} miles - Avg ${round(avg_payment, 2)} per delivery"
                  )
    
def handle_loading_previous_file():
    load_option = input("\nLoad data from (csv/db/skip)? ").strip().lower()

    if load_option == "csv":
        filename = input("Enter the filename (ex: deliveries_2025-04-11.csv): ").strip()
        previous_deliveries = load_deliveries_from_csv(filename)

    elif load_option == "db":
        previous_deliveries = load_deliveries_from_db()

    else:
        return  # skip loading

    if not previous_deliveries:
        return

    use_filter = input("Filter deliveries by date? (y/n): ").strip().lower()
    if use_filter == "y":
        filtered = filter_deliveries_by_date(previous_deliveries)
        if filtered:
            print_summary(filtered)
            zone_summary(filtered)
            calculate_idle_time(filtered)
            zone_performance_by_time(filtered)
        else:
            print("No deliveries match the filter criteria.")
    else:
        print_summary(previous_deliveries)
        zone_summary(previous_deliveries)
        calculate_idle_time(previous_deliveries)
        zone_performance_by_time(previous_deliveries)


def generate_driver_report(state, mpg, earnings, miles, active_minutes=None):
    GAS_PRICE = 4.21 #Can be edited for flexibility
    MIN_WAGE = 20.00 #Prop 22 CA base hourly rate

    gas_cost = (miles / mpg) * GAS_PRICE
    print(f"\n===Driver Report===\n")
    print(f"Total Miles: {round(miles, 1)}")
    print(f"Total Earnings: ${round(earnings, 2)}")
    print(f"Estimated Gas Cost: ${round(gas_cost, 2)}")

    if state.lower() == "california":
        if active_minutes is None:
            print("Prop 22 Calculation Skipped: No active time provided")
            return
        guaranteed = (active_minutes / 60) * MIN_WAGE
        print(f"Prop 22 Guaranteed Earnings: ${round(guaranteed, 2)}")

        if earnings < guaranteed:
            adjustment = guaranteed - earnings
            print(f"Prop 22 Adjustment: ${round(adjustment, 2)}")
        else:
            print("No Prop 22 adjustment required. You're above minimum guaranteed earnings.")

#--- Main Flow ---
zones = log_zones()
handle_loading_previous_file()
log_multiple_deliveries(zones)
print_summary(deliveries)
final_totals()
zone_summary(deliveries)
zone_performance_by_time(deliveries)


calculate_idle_time(deliveries)
save_deliveries_to_db(deliveries)
generate_report = input("\nGenerate Prop 22 / Gas Report? (y/n): ").strip().lower()
if generate_report == "y":
    user_state = input(f"Enter your state (e.g., California): ").strip()
    user_mpg = float(input("Your car's MPG: "))
    session_minutes = int(input("Enter your Active Session time in Minutes: ")) if user_state.lower() == "california" else None
    generate_driver_report(user_state, user_mpg, total_miles, total_earnings, session_minutes)


# Reset totals
total_miles = 0
total_earnings = 0
total_tips = 0