# Import necessary libraries
from flask import Flask, jsonify, request, session
import requests
import gspread
from google.oauth2 import service_account
from datetime import datetime, timedelta
import random
import signal
import sys

# Suppress only the InsecureRequestWarning from urllib3 needed for SSL verification
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Placeholder functions, replace with actual implementations
def get_google_sheets_data(sheet_name):
    # Implement logic to fetch data from Google Sheets
    # Example: Use gspread library and service account credentials
    gc = gspread.service_account(filename='path/to/credentials.json')
    sh = gc.open(sheet_name)
    return sh.get_all_records()

def get_instagram_data(endpoint, params):
    # Implement logic to fetch data from Instagram Graph API
    # Example: Use requests library to make API calls
    url = f'https://graph.instagram.com/v12.0/{endpoint}'
    response = requests.get(url, params=params)
    return response.json()

def search_posts_by_hashtag(hashtag):
    # Implement logic to search recent posts by hashtag
    # Example: Use Instagram Graph API to search for posts
    params = {'q': hashtag, 'access_token': 'your_access_token'}
    return get_instagram_data('ig_hashtag_search', params)

def process_comments(media_id, keyword):
    # Implement logic to process comments and store prospects
    # Example: Fetch comments for a given media id and check if keyword is in bio
    comments_data = get_instagram_data(f'{media_id}/comments', {'access_token': 'your_access_token'})
    for comment in comments_data['data']:
        if keyword in comment.get('text', '').lower():
            # Store username in prospects sheet and update red flag value
            prospect_username = comment['username']
            # Example: Update prospects sheet using gspread

def generate_comments_and_mark_contacted(username):
    # Implement logic to generate comments and mark as contacted
    # Example: Fetch user posts, generate comments, and mark as contacted
    user_posts = get_instagram_data(f'{username}/media', {'access_token': 'your_access_token'})
    # Example: Generate comments
    generated_comments = ["Great post!", "Keep it up!", "Awesome content!"]
    # Example: Mark as contacted in the comment sheet

def check_and_respond_to_dm_inquiries(bot_account):
    # Implement logic to check and respond to DM inquiries
    # Example: Fetch messages from bot account and check for inquiries using DialogFlow
    messages = get_instagram_data(f'{bot_account}/messages', {'access_token': 'your_access_token'})
    for message in messages['data']:
        # Example: Use DialogFlow to check for inquiries and respond accordingly

def follow_up_with_usernames(uncontacted_usernames, contacted_usernames):
    # Implement logic to follow up with usernames
    # Example: Generate comments and schedule follow-ups
    for username in uncontacted_usernames:
        user_posts = get_instagram_data(f'{username}/media', {'access_token': 'your_access_token'})
        # Example: Generate comments and schedule follow-ups

def post_ad_posts_with_tensorflow():
    # Implement logic to post ad posts with TensorFlow model
    # Example: Use TensorFlow model to generate ad posts and post them

def generate_and_post_story():
    # Implement logic to generate and post a story
    # Example: Use Instagram Graph API to post a story

def schedule_posts(posts_type, schedule_date):
    # Implement logic to schedule posts
    # Example: Schedule posts based on specified type and date

# Flask app for DialogFlow fulfillment
app = Flask(__name__)

# Set up a session for storing script and global status
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Placeholder variable for uncontacted and contacted usernames
uncontacted_usernames = [...]  # Replace with actual data
contacted_usernames = [...]  # Replace with actual data

# Main script to execute the Instagram Graph API workflow
def instagram_graph_api_script():
    # Loop for 30 times (Step 7)
    for _ in range(30):
        # 6. If no hashtag id next to hashtag in sheet, get hashtag id
        # (Implementation depends on your specific setup with Instagram Graph API)

        # 7. Search recent posts by hashtag and store data in posts sheets
        for hashtag in hashtags_sheet_data:
            posts_data = search_posts_by_hashtag(hashtag)
            # Store relevant data in posts sheet
        # Set date to run again.

    # 8. Process comments and store prospects
    for post_data in posts_sheet_data:
        process_comments(post_data['media_id'], "keyword")

    # 9. Generate comments and mark as contacted
    for username in comment_sheet_data:
        generate_comments_and_mark_contacted(username)

    # 10. 4x a day, get messages from bot account and respond to inquiries
    for _ in range(4):
        check_and_respond_to_dm_inquiries(bots_sheet_data['bot_account'])

    # 11. For each uncontacted username, get two random posts, generate comment on one, and mark follow-up date
    follow_up_with_usernames(uncontacted_usernames, contacted_usernames)

    # 12. Check if any contacted usernames have a follow-up
    # (Implementation depends on your specific logic for follow-ups)

    # 13. Post batch of ad posts with TensorFlow model
    post_ad_posts_with_tensorflow()

    # 14. Generate and post story
    generate_and_post_story()

    # 15. Check to see if new comments, posts, or stories need to be scheduled
    schedule_posts("comments", datetime.now() + timedelta(days=1))
    schedule_posts("posts", datetime.now() + timedelta(days=2))
    schedule_posts("stories", datetime.now() + timedelta(days=random.randint(1, 3)))


# Example: Function to handle the Dialogflow webhook request
@app.route('/dialogflow-webhook', methods=['POST'])
def dialogflow_webhook():
    req = request.get_json()

    # Placeholder code, replace with actual DialogFlow intent handling
    intent = req['queryResult']['intent']['displayName']
    if intent == 'Inquiry':
        # Implement logic for handling the specific intent, send booking link with chat GPT format
        fulfillment_text = 'Your fulfillment text here.'
    else:
        # Handle other intents if needed
        fulfillment_text = 'Default fulfillment text.'

    return jsonify({'fulfillmentText': fulfillment_text})


# Function to gracefully shutdown Flask server for code updates
def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Perform cleanup tasks if necessary
    sys.exit(0)


# Start the Flask server
if __name__ == '__main__':
    # Set up a signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    app.run(host='0.0.0.0', port=80)  # Start the Flask server for DialogFlow request fulfillment
    # Run the Instagram Graph API script
    instagram_graph_api_script()