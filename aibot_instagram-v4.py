import requests
import random
import gspread
import time
import openai
import stylegan2
import os
import cv2
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

# Define your Instagram accounts and proxy configurations
accounts = [
    {
        "username": "account1",
        "password": "password1",
        "access_token": "access_token1",
        "proxy": {
            "ip": "proxy_ip1",
            "port": "proxy_port1",
            "username": "proxy_username1",
            "password": "proxy_password1"
        }
    },
        # Add more accounts and proxy configurations here
    }
]

# Your Instagram Graph API access token
# Add more access tokens for your accounts if needed
access_tokens = [account["access_token"] for account in accounts]

# Define hashtags to search for
hashtags = ['hashtag1', 'hashtag2', 'hashtag3']

# Define limit for prospecting usernames
prospecting_limit = 400

# Initialize a set to temporarily store prospected usernames
prospected_usernames = set()

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document housing prospects
spreadsheet = client.open('Your Google Sheets Document')
worksheet = spreadsheet.get_worksheet(0)

# Initialize the OpenAI API key
openai.api_key = 'your-openai-api-key'

# Set up Flask app for DialogFlow fulfillment
app = Flask(__name__)

# Flask route for DialogFlow webhook
@app.route('/dialogflow_webhook', methods=['POST'])

# Define a function to find and store 400 unique usernames to Google Sheets document
def find_and_store_usernames():
    for _ in range(prospecting_limit):
        hashtag = random.choice(hashtags)
        next_url = f'https://graph.instagram.com/v13.0/tags/{hashtag}/recent_media?access_token={random.choice(access_tokens)}&count=10'

        while next_url and len(prospected_usernames) < prospecting_limit:
            try:
                account = random.choice(accounts)
                username = account["username"]
                password = account["password"]
                proxy = account["proxy"]

                # Implement code to find usernames and store them in Google Sheets and the set
                session = requests.Session()
                session.proxies = {
                    'http': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}',
                    'https': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
                }

                response = session.get(next_url)
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        for post in data['data']:
                            if 'username' in post.get('caption', {}):
                                username = post['caption']['username']
                                bio = get_user_bio(username)
                                keywords = ["indie game dev", "game dev"]
                                bio_lower = bio.lower()
                                if any(keyword in bio_lower for keyword in keywords):
                                    # Add the username to the set
                                    prospected_usernames.add(username)
                                    # Add the username to Google Sheets
                                    worksheet.append_row([username])  # You can append additional information as needed
                    next_url = data['paging'].get('next')
                else:
                    print("Failed to fetch post data.")
                    break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

# Function to process usernames and send messages
def process_usernames():
    usernames = worksheet.col_values(1)  # Assuming usernames are in the first column
    for username in usernames:
        if username != '' and username != 'Messaged':
            for account in accounts:
                if account["username"] == username:
                    send_dm(username, account["access_token"], account["proxy"])
                    time.sleep(60)  # Sleep to respect Instagram's rate limits
                    break
                    
# Function to create and post a reel
def create_and_post_reel(bot, username, password, proxy_info):
    # Log in to an Instagram account
    bot.login(username=username, password=password, proxy=proxy_info)

    # Generate an image using StyleGAN2
    latent_vector = stylegan2.run.generate_latent()
    image = Gs.run(latent_vector)

    # Generate a caption using ChatGPT
    generated_text = generate_text_with_gpt("Your prompt here")

    # Add the generated text as an overlay to the image
    image_with_overlay = add_text_overlay(image, generated_text)

    # Convert the image to a frame and add it to the video
    frame = cv2.cvtColor(np.array(image_with_overlay), cv2.COLOR_RGB2BGR)
    video_writer.write(frame)

    # Release the VideoWriter
    video_writer.release()

    video_path = 'output_video.mp4'  # Provide the path to your generated video

    # Upload the video to Instagram
    bot.upload_reel(video_path, caption=generated_text)

    # Log out from the account
    bot.logout()
    
# Function to generate a personalized message using ChatGPT
def generate_personalized_message(previous_message):
    global conversation_context
    conversation_context.append(previous_message)

    # Use ChatGPT to create a response based on the conversation context
    response = openai.Completion.create(
        engine="davinci",
        messages=conversation_context,
        max_tokens=50
    )

    # Extract the response message from ChatGPT
    response_message = response.choices[0].message['content'].strip()
    
    return response_message

# Variable to store the conversation context
conversation_context = []

# Function to handle the Dialogflow webhook request
@app.route('/dialogflow-webhook', methods=['POST'])
def dialogflow_webhook():
    req = request.get_json()
    
    # Extract intent and parameters from the Dialogflow request
    intent = req['queryResult']['intent']['displayName']

    if intent == 'BookMeeting':
        # Use ChatGPT to generate a personalized message asking for meeting details
        personalized_message = generate_personalized_message(req['queryResult']['queryText'])

        return jsonify({
            'fulfillmentText': personalized_message
        })
    elif intent == 'CollectMeetingDetails':
        # Extract parameters provided by the user
        date = req['queryResult']['parameters']['date']
        time = req['queryResult']['parameters']['time']
        location = req['queryResult']['parameters']['location']
        # You can now use the collected parameters to book the meeting and provide a response.
        return jsonify({
            'fulfillmentText': f'Great! We have scheduled a meeting on {date} at {time} at {location}.'
        })
    else:
        # Handle other intents here if needed
        return jsonify({'fulfillmentText': 'I am not sure how to respond to that.'})

if name == ‘main’:
    for account in accounts:
        find_and_store_usernames()  # Find and store usernames in Google Sheets
        create_and_post_reel(bot, account, account[“proxy”])
        
    process_usernames()
    
    app.run(host=‘0.0.0.0’, port=80)  # Start the Flask server for DialogFlow
