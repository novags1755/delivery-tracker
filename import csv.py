import csv

filename = "deliveries_2025-04-12.csv"

try:
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print("\n📦 Deliveries loaded from CSV:")
        for row in reader:
            print(row)
except FileNotFoundError:
    print("❌ File not found.")