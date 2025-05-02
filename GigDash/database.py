# database.py
# Database interaction module for GigDash.
# - Creates the 'deliveries' table if it does not exist.
# - Defines functions to fetch and summarize delivery data.
# - (Upcoming) Defines functions to fetch and manipulate delivery data.

# database.py
# Handles SQLite interactions for GigDash, including delivery inserts and summary queries.

import sqlite3
from datetime import datetime
from collections import defaultdict

# === CREATE deliveries TABLE ===
connection = sqlite3.connect('gigdash.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone TEXT NOT NULL,
    pay REAL NOT NULL,
    tip REAL,
    mileage REAL,
    state TEXT NOT NULL,
    date TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
''')

connection.commit()
connection.close()

# === INSERT delivery with timestamp ===
def add_delivery(zone, pay, tip, mileage, state):
    """Insert a new delivery into the deliveries table with date and timestamp."""
    connection = sqlite3.connect('gigdash.db')
    cursor = connection.cursor()

    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO deliveries (zone, pay, tip, mileage, state, date, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (zone, pay, tip, mileage, state, current_date, current_timestamp))

    connection.commit()
    connection.close()

# === FETCH all deliveries ===
def get_deliveries():
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM deliveries')
    deliveries = cursor.fetchall()
    connection.close()
    return deliveries

# === TOTALS ===
def get_totals():
    connection = sqlite3.connect('gigdash.db')
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(pay), SUM(tip), SUM(mileage) FROM deliveries')
    totals = cursor.fetchone()
    connection.close()
    return totals

# === DATE RANGE REPORT ===
def generate_report(start_date, end_date):
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('''
        SELECT date, pay, tip, mileage FROM deliveries
        WHERE date BETWEEN ? AND ?
    ''', (start_date, end_date))
    deliveries = cursor.fetchall()
    connection.close()

    report = defaultdict(lambda: {'pay': 0, 'tip': 0.0, 'mileage': 0.0, 'deliveries': 0})
    for d in deliveries:
        date = d['date']
        report[date]["deliveries"] += 1
        report[date]["pay"] += d['pay']
        report[date]["tip"] += d["tip"]
        report[date]["mileage"] += d["mileage"]

    return {
        "deliveries": dict(report),
        "start": start_date,
        "end": end_date
    }

# === WEEKLY REPORT ===
def generate_weekly_report():
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT date, pay, tip, mileage FROM deliveries')
    deliveries = cursor.fetchall()
    connection.close()

    report = defaultdict(lambda: {'deliveries':0, 'pay':0.0, 'tip':0.0, 'mileage':0.0})
    for d in deliveries:
        date_obj = datetime.strptime(d['date'], '%Y-%m-%d')
        week_key = date_obj.strftime('%Y-W%W')
        report[week_key]['deliveries'] += 1
        report[week_key]['pay'] += d['pay']
        report[week_key]['tip'] += d['tip']
        report[week_key]['mileage'] += d['mileage']

    sorted_weeks = sorted(report.items())
    insights = {
        "best_week": None,
        "comparison": []
    }

    highest = 0
    for i, (week, data) in enumerate(sorted_weeks):
        total = data['pay']
        if total > highest:
            highest = total
            insights["best_week"] = {"week": week, "earnings": total}

        if i > 0:
            prev_week, prev_data = sorted_weeks[i - 1]
            prev_total = prev_data['pay']
            delta = round(((total - prev_total) / prev_total) * 100, 2) if prev_total else None
            insights["comparison"].append({
                "week": week,
                "earnings": total,
                "change_vs_prev": delta
            })
        else:
            insights["comparison"].append({
                "week": week,
                "earnings": total,
                "change_vs_prev": None
            })

    return dict(report), insights

# === MONTHLY REPORT ===
def generate_monthly_report():
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT date, pay, tip, mileage FROM deliveries')
    deliveries = cursor.fetchall()
    connection.close()

    report = defaultdict(lambda: {'deliveries': 0, 'pay': 0.0, 'tip': 0.0, 'mileage': 0.0})
    for d in deliveries:
        date_obj = datetime.strptime(d['date'], '%Y-%m-%d')
        month_key = date_obj.strftime('%Y-%m')
        report[month_key]['deliveries'] += 1
        report[month_key]['pay'] += d['pay']
        report[month_key]['tip'] += d['tip']
        report[month_key]['mileage'] += d['mileage']

    sorted_months = sorted(report.items())
    insights = {
        "best_month": None,
        "comparison": []
    }

    highest = 0
    for i, (month, data) in enumerate(sorted_months):
        total = data["pay"]
        if total > highest:
            highest = total
            insights["best_month"] = {"month": month, "earnings": total}

        if i > 0:
            prev_month, prev_data = sorted_months[i - 1]
            prev_total = prev_data["pay"]
            delta = round(((total - prev_total) / prev_total) * 100, 2) if prev_total else None
            insights["comparison"].append({
                "month": month,
                "earnings": total,
                "change_vs_prev": delta
            })
        else:
            insights["comparison"].append({
                "month": month,
                "earnings": total,
                "change_vs_prev": None
            })

    return dict(report), insights

# === ZONE REPORT ===
def generate_zone_report():
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT zone, pay FROM deliveries')
    deliveries = cursor.fetchall()
    connection.close()

    report = defaultdict(lambda: {'pay': 0.0, 'count': 0})
    best_zone = None
    highest_avg = 0

    for d in deliveries:
        zone = d['zone']
        report[zone]['pay'] += d['pay']
        report[zone]['count'] += 1

    for zone, data in report.items():
        avg = data['pay'] / data['count'] if data['count'] else 0
        data['avg'] = round(avg, 2)

        if avg > highest_avg:
            highest_avg = avg
            best_zone = {
                'zone': zone,
                'avg': round(avg, 2)
            }

    return dict(report), best_zone
def generate_idle_time_report():
    """Calculate time gaps between deliveries (idle time)."""
    connection = sqlite3.connect('gigdash.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute('SELECT timestamp FROM deliveries ORDER BY timestamp')
    rows = cursor.fetchall()
    connection.close()

    idle_times = []
    previous = None

    for row in rows:
        current = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')

        if previous:
            delta = current - previous
            minutes = round(delta.total_seconds() / 60, 2)
            idle_times.append(minutes)

        previous = current

    average_idle = round(sum(idle_times) / len(idle_times), 2) if idle_times else 0

    return {
        'idle_times': idle_times,
        'average_idle': average_idle
    }
