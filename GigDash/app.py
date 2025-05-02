# app.py
# Main Flask application that handles web routes for GigDash.
# - Renders the home page with the delivery form.
# - Accepts submitted deliveries via POST requests.
# - Calls database functions to store the submitted delivery data.

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from database import add_delivery, get_deliveries, get_totals
import sqlite3
from database import generate_report, generate_weekly_report, generate_monthly_report, generate_zone_report, generate_idle_time_report



app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_delivery', methods=['POST'])
def submit_delivery():
    zone = request.form['zone']
    pay = float(request.form['pay'])
    tip = float(request.form['tip'])
    mileage = float(request.form['mileage'])
    state = request.form['state']



    add_delivery(zone,pay,tip,mileage,state)
    flash('Delivery added successfully!')

    return redirect(url_for('home'))

@app.route('/deliveries')
def deliveries():
    all_deliveries = get_deliveries()
    totals = get_totals()

    # Get MPG and gas price from query params or set defaults
    try:
        mpg = float(request.args.get('mpg', 25))
        gas_price = float(request.args.get('gas', 5.00))
    except:
        mpg = 25
        gas_price = 5.00

    prop22, gas_cost = calculate_prop22_and_gas(all_deliveries, mpg, gas_price)

    return render_template(
        'deliveries.html',
        deliveries=all_deliveries,
        totals=totals,
        prop22=prop22,
        gas_cost=gas_cost,
        mpg=mpg,
        gas_price=gas_price
    )

def calculate_prop22_and_gas(deliveries, mpg=25, gas_price=5.00):
    """Returns estimated Prop 22 adjusment and gas cost based on mileage."""
    total_miles= sum([d['mileage'] for d in deliveries])
    prop22 = round(total_miles * 0.34, 2) # Prop 22 adjustment
    gas_cost = round((total_miles / mpg) * gas_price, 2)
    return prop22, gas_cost


@app.route('/delete_delivery/<int:delivery_id>', methods=['POST'])
def delete_delivery(delivery_id):
    connection = sqlite3.connect('gigdash.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM deliveries WHERE id = ?', (delivery_id,))
    connection.commit()
    connection.close()
    
    flash('Delivery deleted successfully!')
    return redirect(url_for('deliveries'))

@app.route('/report',  methods=['GET','POST'])
def report():
    report_data = {}
    start_date = end_date = ""

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        report_data = generate_report(start_date, end_date)
    
    return render_template('report.html', report_data=report_data, start_date=start_date, end_date=end_date)

@app.route('/weekly_report')

def weekly_report():
    report, insights = generate_weekly_report()
    return render_template('weekly_report.html', report=report, insights=insights)


@app.route('/monthly_report')

def monthly_report():
    report, insights = generate_monthly_report()
    return render_template('monthly_report.html', report=report , insights=insights)

@app.route('/zones')
def zone_report():
    report, best_zone = generate_zone_report()
    return render_template('zone_report.html', report=report, best_zone=best_zone)


@app.route('/idle')
def idle_report():
    report = generate_idle_time_report()
    return render_template('idle_report.html', report=report)


if __name__ == "__main__":
    app.run(debug=True)