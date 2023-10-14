import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import time

#----------------------------------------------------------------------------------------------------------------
# Environment Setup:
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

# Initialize OpenAI with your API key
api_key = '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'
openai.api_key = api_key

#----------------------------------------------------------------------------------------------------------------
# Function Definitions:

# Function to generate DM content using GPT-3
def generate_meeting_request_dm(account_username):
    # Define a structured message template
    template = {
        'intro': f"Hi {account_username}, I hope this message finds you well. I found you on Twitter and thought we could connect.",
        'social_proof': "I actually specialize in [service].",
        'mechanism': "What sets us apart is that our service not only covers ad spend but is also tailored to the gaming industry.",
        'cta': "Would you be interested in learning more? Here's a link to our Video Sales Letter (VSL): [insert VSL link]",
    }

    # Replace placeholders in the template with the account's username
    for key, value in template.items():
        template[key] = value.replace('[service]', 'indie game development').format(account_username=account_username)

    # Combine the template steps into the full message
    full_message = "\n".join(template.values())

    # Send the message template to GPT-3 for content generation
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=full_message,
        max_tokens=100
    )

    # Retrieve the AI-generated content
    generated_content = response.choices[0].text.strip()
    return generated_content

# Function to search for accounts using a hashtag, filter based on bio, and send DMs
def search_hashtag_filter_bio_and_send_dms(api, hashtag, daily_dm_limit=40, bio_phrases=['indie game dev']):
    for tweet in tweepy.Cursor(api.search_tweets, q=f"#{hashtag}", lang="en").items():
        account_username = tweet.user.screen_name
        user_bio = tweet.user.description.lower()

        if any(phrase in user_bio for phrase in bio_phrases):
            dm_content = generate_meeting_request_dm(account_username)
            api.send_direct_message(screen_name=account_username, text=dm_content)
            daily_dm_limit -= 1

            if daily_dm_limit == 0:
                break

#----------------------------------------------------------------------------------------------------------------
# Main Code:

# Twitter API constant credentials
consumer_key = 'TDRZejJIRUZXczMzTURYXzluTWk6MTpjaQ'
consumer_secret = 'ETplZ_Jrp0dxDMME1E3d8vXeVolB55mtqvOHrBpGevDRq810u1'

# Loop through the Twitter accounts and their access tokens
for row in data:
    access_token = row["Access Token"]
    access_token_secret = row["Access Token Secret"]

    # Initialize Twitter API for the current account
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Execute the DM-sending logic for each account
    search_hashtag_filter_bio_and_send_dms(api, "indie game dev")
