# Import necessary libraries
import requests
import random
import gspread
import openai
from google.oauth2.service_account import ServiceAccountCredentials
from flask import Flask

# Define bot account info for all 10 bot accounts
accounts = [
    {
        "username": "account1",
        "password": "password1",
        "proxy": {
            "ip": "proxy_ip1",
            "port": "proxy_port1",
            "username": "proxy_username1",
            "password": "proxy_password1"
        },
    },
    # Add details for the other 9 accounts
]

# Define IG Graph API access tokens
access_tokens = ["access_token1", "access_token2", "access_token3"]  # Add more if needed

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
@app.route('/webhook', methods=['POST'])
def webhook():
    # Implement intent handling here
    # Generate response based on detected intent
    return jsonify({'fulfillmentText': 'Response from DialogFlow'})
    
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

                # Implement code to find usernames and store them in Google Sheets

                next_url = data['paging'].get('next')
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
# Function to send a DM using a specific account and proxy
def send_dm(username, access_token, proxy_info):
    proxy = proxy_info["proxy"]
    session = requests.Session()

    # Set up proxy for this request
    session.proxies = {
        'http': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}',
        'https': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port"]}'
    }

    # Define a structured message template
    template = {
        'intro': f"Hi {username}, I'm looking to connect with other indie game devs on Instagram and thought we could chat!",
        'social_proof': "I know this is random, but I actually specialize in boosting revenue using tailored funnels for game devs and streamers.",
        'mechanism': "One thing that makes us so different is we're so sure of our process we give you free ad spend.",
        'cta': "And more revenue means more dev time! Here's a quick run down on how we do it: [https://rb.gy/vaypj]",
    }

    # Replace placeholders in the template with the account's username
    for key, value in template.items():
        template[key] = value.format(username=username)

    # Combine the template steps into the full message
    full_message = "\n".join(template.values)

    # Generate additional content using GPT-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=full_message,
        max_tokens=100
    )
    generated_message = response.choices[0].text.strip()

    # Construct the DM data
    dm_data = {
        'recipient_user_id': username,
        'message': generated_message
    }

    # Send the DM using the Instagram Graph API
    response = session.post(f'https://graph.instagram.com/v13.0/me/media/abc123/messages?access_token={access_token}', json=dm_data)

    if response.status_code == 200:
        print(f'Sent DM to {username}: {generated_message}')
        cell = worksheet.find(username)
        worksheet.update_cell(cell.row, cell.col + 1, 'Messaged')
        return True
    else:
        print(f'Failed to send DM to {username}: {response.text}')
        return False
        
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

