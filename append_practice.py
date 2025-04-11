#append practice
items = []
print("Type anything you want. Type 'done' to finish.\n")

while True:
    entry = input("Enter Item:")
    if entry.lower() == "done":
        break
    items.append(entry)
    print("Current list:", items)

print("\nFinal list of items you added:")
for i, item in enumerate(items,1):
    print(f"{i}.{item}")


#practice 2
zones = []

num_zones = int(input("How many Zones do you want to log?"))
for i in range(num_zones):
    z = input("Enter zone name:")
    zones.append(z)

print("\nZones logged today:")
for i,z in enumerate(zones,1):
    print(f"{i}. {z}")

#Drill number 3

zones= []

num_zones = int(input("How many zones?"))
for i in range(num_zones):
    z = input("Enter zone name:")
    zones.append(z)

print("\nZones you logged today:")
for i, zone in enumerate(zones,1):
    print("f{i}.{zone}")

deliveries = []
num_deliveries = int(input("\nHow many Deliveries do you want to log?"))

for i in range(num_deliveries):
    print(f"\n---Delivery #{i+1}---")

    for j, zone in enumerate(zones,1):
        print(f"{j}.{zone}")
    zone_choice = int(input("Select zone number:"))
    zone_name = zones[zone_choice -1]

    miles = float(input("Miles driven: "))
    payment = float(input("Total Payment: $"))
    tip = float(input("Tip received: $"))

    delivery = {
        "zone": zone_name,
        "miles": miles,
        "payment": payment,
        "tip": tip,
    }
    deliveries.append(delivery)

print("\n---All Deliveries ---")
for d in deliveries:
    print(f"Zone: {d['zone']}|Miles: {d['miles']}| Payment: ${d['payment']}| Tip: ${d['tip']}")
    
