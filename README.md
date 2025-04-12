# 🚗 DashTrack (v1.1)

**Author:** Gio  
**Type:** Python CLI Tool  
**Status:** Stable Release (`v1.1`)  
**License:** MIT  

---

## 📦 What is DashTrack?

**DashTrack** is a command-line tool built in Python to help gig workers (like DoorDash drivers) **track deliveries**, **calculate earnings**, and **export daily logs** as CSV files.  
No fancy UI — just real logic, clean backend, and efficient data tracking.

---

## 🎯 Features

- 🔄 Log multiple delivery zones and sessions
- 🧾 Calculate earnings, miles, and tip totals
- 📊 Show detailed summaries and cost per mile
- 🗂 Export delivery data to `.csv` for backup or analysis
- 📥 Load and filter past logs by **specific date or date range**
- 📌 Zone-based breakdowns included

---

## 🖥️ How to Run

```bash
python delivery_tracker.py


You'll be prompted step-by-step through zones, deliveries, time entries, and notes. The program saves everything in a dated .csv file like:

Copy
Edit
deliveries_2025-04-11.csv
📁 Sample Output
text
Copy
Edit
=== Overall Summary ===
Total Deliveries Logged: 4
Total Miles Driven: 26.5
Total Earnings: $65.75
Total Tips Earned: $15.50
Average Earnings per Mile: $2.48

=== Zone Breakdown ===
Tarzana: 2 deliveries - $32.25 earned - 11.0 miles
Northridge: 2 deliveries - $33.50 earned - 15.5 miles
⚙️ Tech Stack
Python 3.x

CSV module

Datetime module

Fully modular function-based design

CLI only (no Flask/Django yet)

🚀 Roadmap
 CLI Logger & Calculator

 CSV Save & Load

 Date Filtering (single & range)

 Zone Summary

 Flask Web Version (coming soon)

 SQLite Upgrade

👀 Want to Try It?
Just clone the repo, run python delivery_tracker.py, and start logging your day.

🤝 License
MIT — free to use, fork, improve, and build on it. Credit appreciated.

💬 Dev Notes
This tool was handcrafted as part of my backend development journey. It’s built for real daily use, and every feature was tested with real delivery data.
Built with logic. Built with purpose. Built to grow.

yaml
Copy
Edit

---

## ✅ Next Steps:
1. Drop that into your GitHub repo as `README.md`
2. Add + commit your code and README
3. Tag the commit:
```bash
git add .
git commit -m "Release v1.0 — DashTrack CLI tool complete"
git push

## 🚀 DashTrack v1.1 – CLI Delivery Tracker

A command-line tool to help gig drivers log and analyze delivery sessions with zone tracking, tips, mileage, and CSV export.

---

### ✅ What’s New in v1.1
- **Append Mode:** Automatically appends new deliveries to today's `.csv` file instead of overwriting
- **Header Check:** Adds headers only if the file doesn’t exist
- **Same-day Logging Support:** Allows multiple runs during the same day

---

### 🔧 Features
- Zone selection with multi-delivery logging
- Calculates tips, CPM, duration, totals
- Daily `.csv` log generation with clean formatting
- Load previous logs and filter by date
- Shows per-zone delivery summary

---

### 📂 Example Output File: `deliveries_2025-04-12.csv`
```csv
zone,miles,payment,tip,cpm,start,end,duration,notes
Valencia,4.5,12.75,3.25,2.83,9:00 AM,9:25 AM,25,Starbucks
...
🔄 Coming Soon (Future Versions)
SQLite database logging

GUI (Tkinter/PyQT)

Earnings analytics dashboard

yaml
Copy
Edit

Copy/paste that into your `README.md`, and feel free to tweak the wording however you want.

---

## ✅ 3. Push Your Changes to GitHub

If you're inside VS Code:
```bash
git add .
git commit -m "🚀 v1.1 - Added append mode + file header check"
git push