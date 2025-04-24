# DashTrack 🛵📊

**DashTrack** is a CLI-based delivery tracking tool built by Gio to track DoorDash sessions and analyze delivery performance. This tool helps independent drivers log key session data, calculate earnings, track idle time, and estimate Prop 22 adjustments (for CA drivers). Now fully refactored and database-powered with SQLite!

---

## 🚀 Features

- Log delivery details (zone, miles, time, pay, tips)
- View zone performance by time of day
- Calculate idle time between deliveries
- Estimate **Prop 22** wage adjustments (California only)
- Save & load deliveries from a **SQLite database**
- Optional CSV loading for backward compatibility
- Daily session report with gas usage & MPG input
- Full **error handling** for user inputs

---

## 📂 Database Schema (SQLite)

- `zones` table (id, name)
- `deliveries` table (zone_id FK, miles, payment, tip, cpm, start_time, end_time, duration, notes)

---

## 🔧 Installation

```bash
git clone https://github.com/novags1755/delivery-tracker.git
cd delivery-tracker
python dashtrack.py
Ensure you have Python 3.9+ and sqlite3 installed (comes by default).

🛠 Usage
Start the script:

bash
Copy
Edit
python dashtrack.py
Choose to load past data or log new deliveries

Enter zone names, delivery details, and session stats

View summaries, breakdowns, and optionally generate a Prop 22 + Gas report

🧪 Sample Output
text
Copy
Edit
Zone: Northridge
Miles: 5.4
Payment: $12.50
Tip: $2.50
Cost per Mile: $2.31
Time: 6:45 AM to 7:05 AM
Duration: 20.0 minutes
📜 License
This project is licensed under the MIT License.

✨ Author
Built by Gio aka novags1755 as part of his backend development journey.
Follow the journey & projects: github.com/novags1755