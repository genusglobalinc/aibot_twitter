import requests
import random
import gspread
import time
import openai

# Your Instagram Graph API access token
access_token = 'your-access-token'

# List of different hashtags
hashtags = ['hashtag1', 'hashtag2', 'hashtag3']

# Maximum number of posts to retrieve (adjust as needed)
max_posts = 1000

# Initialize a set to store retrieved usernames
retrieved_usernames = set()

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document containing the list of usernames
spreadsheet = client.open('Your Instagram Usernames Document')
worksheet = spreadsheet.get_worksheet(0)

# Instagram Graph API access token
access_token = 'your-instagram-access-token'

# Proxy information
proxy_ip = 'your-proxy-ip'
proxy_port = 'your-proxy-port'
proxy_user = 'your-username'
proxy_pass = 'your-password'

# Initialize the OpenAI API key
openai.api_key = 'your-openai-api-key'

# Function to validate and store usernames based on bio
def validate_and_store_usernames():
    for _ in range(10):  # You can adjust the number of runs
        hashtag = random.choice(hashtags)
        next_url = f'https://graph.instagram.com/v13.0/tags/{hashtag}/recent_media?access_token={access_token}&count=10'

        while next_url and len(retrieved_usernames) < max_posts:
            try:
                # Create a session with the proxy
                session = requests.Session()
                session.proxies = {
                    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}',
                    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}'
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
                                    retrieved_usernames.add(username)
                    next_url = data['paging'].get('next')
                else:
                    print("Failed to fetch post data.")
                    break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

# Function to generate and send a DM message using ChatGPT
def generate_and_send_dm(username, access_token):
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
    full_message = "\n".join(template.values())

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
        return True
    else:
        print(f'Failed to send DM to {username}: {response.text}')
        return False

# Function to mark a username as "messaged" in the Google Sheets document
def mark_as_messaged(username):
    cell = worksheet.find(username)
    worksheet.update_cell(cell.row, cell.col + 1, 'Messaged')

# Function to iterate through and process usernames
def process_usernames():
    usernames = worksheet.col_values(1)  # Assuming usernames are in the first column
    for username in usernames:
        if username != '' and username != 'Messaged':
            if generate_and_send_dm(username, access_token):
                mark_as_messaged(username)
            time.sleep(60)  # Sleep to respect Instagram's rate limits

# Main program
if __name__ == '__main':
    validate_and_store_usernames()
    process_usernames()