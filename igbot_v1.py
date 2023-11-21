import requests
import sys
import random
import gspread
import signal
import time
import openai
import os
from google.oauth2 import service_account
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
from dotenv import load_dotenv

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

script_enabled = False
total_bookings = 0
outreach_done = 0
prospecting_limit = 4000
prospected_usernames = set()
conversation_context = []
hashtags = ['indiegamedev', 'indiedev', 'gamedev', 'solodev']

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

g_status = "Idle"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_path = os.environ.get('GOOGLE_SHEETS_CREDS_PATH')

if creds_path:
    creds = service_account.Credentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
else:
    print("Please set the GOOGLE_SHEETS_CREDS_PATH environment variable.")

spreadsheet_accounts = client.open('Prospected Usernames and Bot Accounts')
worksheet_accounts = spreadsheet_accounts.get_worksheet(1)

accounts_data = worksheet_accounts.get_all_records()
accounts = [{"username": row["Username"], "password": row["Password"], "access_token": row["Access Token"]} for row in accounts_data]

zrowsAPI = os.environ.get("ZENROWSAPIKEY")
res_proxy = f"http://{zrowsAPI}:premium_proxy=true&proxy_country=us@proxy.zenrows.com:8001"
res_proxies = {"http": res_proxy, "https": res_proxy}

spreadsheet_usernames = client.open('Prospected Usernames and Bot Accounts')
worksheet_usernames = spreadsheet_usernames.get_worksheet(0)
access_tokens = [account["access_token"] for account in accounts]
DIALOGFLOW_KEY_FILE = os.environ.get("DIALOGFLOW_KEY_FILE")

try:
    credentials = service_account.Credentials.from_service_account_file(DIALOGFLOW_KEY_FILE, scopes=scope)
    client = gspread.authorize(credentials)
except GoogleAuthError as e:
    print(f"Error initializing Google Sheets client: {e}")

@app.route('/dialogflow-webhook', methods=['POST'])
def dialogflow_webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']

    if intent == 'BookMeeting':
        personalized_message = generate_personalized_message(req['queryResult']['queryText'])
        return jsonify({'fulfillmentText': personalized_message})
    elif intent == 'CollectMeetingDetails':
        date, time, location = req['queryResult']['parameters']['date'], req['queryResult']['parameters']['time'], req['queryResult']['parameters']['location']
        bookings += 1
        return jsonify({'fulfillmentText': f'Great! We have scheduled a meeting on {date} at {time} at {location}.'})
    else:
        return jsonify({'fulfillmentText': "I am not sure how to respond to that, but it's always easier to talk in person. Just click here, and pick the best time and method that works for you! Hope to chat soon: https://calendly.com/genusglobal/studios."})

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    sys.exit(0)

@app.route('/control_panel')
def control_panel():
    script_status = session.get('script_enabled', False)
    global_status = session.get('global_status', g_status)
    meetings_booked = 0
    outreach_count = outreach_done
    return render_template('control_panel.html', script_status=script_status, meetings_booked=meetings_booked, outreach_count=outreach_count, global_status=global_status)

@app.route('/update_global_status/<status>')
def update_global_status(status):
    global g_status
    g_status = status
    session['global_status'] = g_status
    return redirect(url_for('control_panel'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("Shutting down gracefully...")
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

@app.route('/toggle_script', methods=['POST'])
def toggle_script():
    global script_enabled
    script_enabled = not script_enabled

    if script_enabled:
        run_script()

    session['script_enabled'] = script_enabled
    return redirect(url_for('control_panel'))

@app.route('/increase_outreach', methods=['POST'])
def increase_outreach():
    global prospecting_limit
    if script_enabled:
        prospecting_limit += 1
    return redirect(url_for('control_panel'))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    app.run(host='0.0.0.0', port=80)

interval_seconds = 24 * 60 * 60

while True:
    current_time = datetime.datetime.now()

    if current_time.weekday() < 5:
        run_script()

    time.sleep(interval_seconds)