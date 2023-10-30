import requests
import random

# Your Instagram Graph API access token
access_token = 'your-access-token'

# List of different hashtags
hashtags = ['hashtag1', 'hashtag2', 'hashtag3']

# Maximum number of posts to retrieve (adjust as needed)
max_posts = 1000

# Initialize a set to store retrieved usernames
retrieved_usernames = set()

# Run through different hashtags
for _ in range(10):  # You can adjust the number of runs
    # Randomly select a hashtag from the list
    hashtag = random.choice(hashtags)
    
    # Set up pagination
    next_url = f'https://graph.instagram.com/v13.0/tags/{hashtag}/recent_media?access_token={access_token}&count=10'
    
    while next_url and len(retrieved_usernames) < max_posts:
        try:
            response = requests.get(next_url)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for post in data['data']:
                        if 'username' in post['caption']:
                            retrieved_usernames.add(post['caption']['username'])
                if 'paging' in data and 'next' in data['paging']:
                    next_url = data['paging']['next']
                else:
                    next_url = None
            else:
                print("Failed to fetch post data.")
                break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

# Convert the set back to a list for further processing
unique_usernames = list(retrieved_usernames)

# Ensure you have a list of around 400 unique usernames to message
if len(unique_usernames) >= 400:
    usernames_to_message = unique_usernames[:400]
else:
    print("Not enough unique usernames collected.")

# Print the usernames to message
for username in usernames_to_message:
    print(username)