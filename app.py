import gspread
import os
import json
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime  # Import datetime module
import pytz  # Import pytz to handle timezones
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Add ProxyFix middleware to handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Authenticate with Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('splendid-sunset-436122-n9-2a123c008b07.json', scopes=SCOPES)

# Connect to the Google Sheet
gc = gspread.authorize(CREDS)
spreadsheet_id = '1E23LKIu2Rcq6vTf2QNg3SVgMTkVaefLiMs4AEjssuA0'
spreadsheet = gc.open_by_key(spreadsheet_id)

def get_or_create_sheet(spreadsheet, sheet_name):
    """Check if a sheet with the given name exists, otherwise create it."""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)  # Try to open the sheet
    except gspread.exceptions.WorksheetNotFound:
        # If the sheet doesn't exist, create it and set up the headers
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="5")
        worksheet.append_row(["User Type", "Name", "Action", "Date", "Time"])  # Add headers
    return worksheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/name', methods=['POST'])
def name():
    user_type = request.form['user_type']
    return render_template('name.html', user_type=user_type)

@app.route('/signinout', methods=['POST'])
def signinout():
    name = request.form['name']
    user_type = request.form['user_type']
    return render_template('signinout.html', name=name, user_type=user_type)

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    name = request.form['name']
    user_type = request.form['user_type']

    # Define the Vancouver time zone
    vancouver_tz = pytz.timezone('America/Vancouver')
    
    # Get the current date and time in Vancouver time zone
    current_time = datetime.now(vancouver_tz)
    
    # Separate the date and time
    current_date = current_time.strftime('%Y-%m-%d')
    current_time_formatted = current_time.strftime('%I:%M %p')  # 1:29 PM format

    # Use the current date as the sheet name (e.g., "2024-09-20")
    sheet_name = current_date

    # Get the sheet for the current date or create one if it doesn't exist
    worksheet = get_or_create_sheet(spreadsheet, sheet_name)

    # Append the data to the sheet
    worksheet.append_row([user_type, name, action, current_date, current_time_formatted])

    # After submission, redirect back to the start
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
