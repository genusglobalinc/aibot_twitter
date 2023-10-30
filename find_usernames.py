import requests
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

def validate_and_store_usernames():
    for _ in range(10):  # You can adjust the number of runs
        hashtag = random.choice(hashtags)
        next_url = f'https://graph.instagram.com/v13.0/tags/{hashtag}/recent_media?access_token={access_token}&count=10'

        while next_url and len(retrieved_usernames) < max_posts:
            try:
                response = requests.get(next_url)
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        for post in data['data']:
                            if 'username' in post.get('caption', {}):
                                username = post['caption']['username']
                                retrieved_usernames.add(username)
                    next_url = data['paging'].get('next')
                else:
                    print("Failed to fetch post data.")
                    break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

if __name__ == '__main':
    validate_and_store_usernames()