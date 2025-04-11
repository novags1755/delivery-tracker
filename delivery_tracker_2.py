# Baby Delivery Tracker v0.1.2
#author: Gio
#Features: Zone logging, time tracking, tips, earnings, average cost per mile


from datetime import datetime

print("Welcome to the Delivery Tracker!")

# Global Totals
total_miles = 0
total_earnings = 0
total_tips = 0
deliveries = []

#--- Define Functions---
def log_zones():
    zones = []
    num_zones = int(input("How many zones do you want to log? "))
    for i in range(num_zones):
        zone = input(f"Enter zone #{i+1} name: ").strip()
        zones.append(zone)
    return zones

def log_delivery(zones):
    #show zones for selection
    print("\nAvailable Zones:")
    for j, zone in enumerate(zones, 1):
        print(f"{j}. {zone}")
    zone_choice = int(input("Select zone number: "))
    zone_name = zones[zone_choice - 1]

    miles = float(input("Miles Driven:"))
    payment = float(input("Total payment ($):"))
    tip = float(input("Tip received ($):"))

    start_time = input("Enter start time (e.g., 6:45 AM): ")
    start_dt = datetime.strptime(start_time, "%I:%M %p")
    end_time = input("Enter end time (e.g., 7:05 AM): ")
    end_dt = datetime.strptime(end_time, "%I:%M %p")
    duration = end_dt - start_dt
    duration_minutes = duration.total_seconds() / 60

    notes = input("Any notes (merchant, special request, etc)? ")
    cost_per_mile = round(payment / miles, 2)

    return{
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
    global total_miles,total_earnings,total_tips
    num_deliveries = int(input("\nHow many deliveries do you want to log? "))
    for i in range(num_deliveries):
         print(f"\n---Delivery #{i+1}---")
         delivery = log_delivery(zones)
         deliveries.append(delivery)
         total_miles += delivery ["miles"]
         total_earnings += delivery ["payment"]
         total_tips += delivery["tip"]


# Print delivery summaries
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

def final_totals ():
    print("\n=== Overall Summary ===")
    print(f"Total Deliveries Logged: {len(deliveries)}")
    print(f"Total Miles Driven: {total_miles}")
    print(f"Total Earnings: ${round(total_earnings, 2)}")
    print(f"Total Tips Earned: ${round(total_tips, 2)}")
    print(f"Average Earnings per Mile: ${round(total_earnings / total_miles, 2)}")

#---Main Program Flow ---
zones = log_zones()
log_multiple_deliveries(zones)
print_summary(deliveries)  
final_totals()

# Optional cleanup for next run
total_miles = 0
total_earnings = 0
total_tips = 0
