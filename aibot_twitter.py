import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import time

#----------------------------------------------------------------------------------------------------------------
# Function Definitions:

# Function to send a standard Direct Message using Twitter API v1.1
def send_standard_dm(api, recipient_id, message):
    try:
        url = f'https://api.twitter.com/1.1/direct_messages/events/new.json'
        data = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": recipient_id
                    },
                    "message_data": {
                        "text": message
                    }
                }
            }
        }
        response = api.request('POST', url, json=data)
        if response.status_code == 200:
            print(f"Direct message sent to recipient {recipient_id}")
        else:
            print(f"Failed to send DM to recipient {recipient_id}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Failed to send DM to recipient {recipient_id}: {e}")

# Function to generate DM content using GPT-3
def generate_meeting_request_dm(account_username):
    # Define a structured message template
    template = {
        'intro': f"Hi {account_username}, I hope this message finds you well. I found you on Twitter and thought we could connect.",
        'social_proof': "I actually specialize in indie game development.",
        'mechanism': "What sets us apart is that our service not only covers ad spend but is also tailored to the gaming industry.",
        'cta': "Would you be interested in learning more? Here's a link to our Video Sales Letter (VSL): [insert VSL link]",
    }

    # Replace placeholders in the template with the account's username
    for key, value in template.items():
        template[key] = value.format(account_username=account_username)

    # Combine the template steps into the full message
    full_message = "\n".join(template.values())
    full_message

    # Generate additional content using GPT-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=full_message,
        max_tokens=100
    )
    generated_content = response.choices[0].text.strip()

    return generated_content

# Function to search for accounts using a hashtag, filter based on bio, and send DMs
def search_hashtag_filter_bio_and_send_dms(api, hashtag, daily_dm_limit=40, bio_keywords=['indie game dev']):
    for tweet in tweepy.Cursor(api.search, q=f"#{hashtag}", lang="en").items():
        # Extract the user's screen name and user ID
        account_username = tweet.user.screen_name
        recipient_id = tweet.user.id
        user_bio = tweet.user.description.lower()

        if any(keyword in user_bio for keyword in bio_keywords):
            dm_content = generate_meeting_request_dm(account_username)
            send_standard_dm(api, recipient_id, dm_content)
            daily_dm_limit -= 1

            if daily_dm_limit == 0:
                break

#----------------------------------------------------------------------------------------------------------------
# Main Code:

# Initialize OpenAI with your API key
api_key = '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'
openai.api_key = api_key

# Twitter API constant credentials
consumer_key = '7G6aj7rnvqA26D6dwy2kvK2ui'
consumer_secret = 'rX5mcADDJn8XswQ8bBiE6CdgUfFIh94Y8qcRyoLgHPyiRTL2MY'

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('ai-bot-twitter-08dd107ad8e6.json', scope)
client = gspread.authorize(creds)

# Access the spreadsheet by its title or URL
spreadsheet = client.open('Twitter Accounts')

# Select a specific worksheet
worksheet = spreadsheet.worksheet('Sheet1')

# Read Twitter API credentials from the spreadsheet
data = worksheet.get_all_records()

# Loop through the Twitter accounts and their access tokens
for row in data:
    access_token = row["Access Token"]
    access_token_secret = row["Access Token Secret"]

    # Initialize Twitter API for the current account
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Execute the DM-sending logic for each account
    search_hashtag_filter_bio_and_send_dms(api, "indiegamedev")
