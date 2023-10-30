import requests
import gspread
import time
import openai

# Initialize the OpenAI API key
openai.api_key = 'your-openai-api-key'

# List of Instagram accounts
instagram_accounts = [
    {
        'access_token': 'account1-access-token',
        'username': 'account1-username',
    },
    {
        'access_token': 'account2-access-token',
        'username': 'account2-username',
    },
    # Add more Instagram accounts as needed
]

# Function to generate and send a DM message using ChatGPT
def generate_and_send_dm(username, account):
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

    # Send the DM using the Instagram Graph API with the selected account's access token
    response = requests.post(f'https://graph.instagram.com/v13.0/me/media/abc123/messages?access_token={account["access_token"]}', json=dm_data)

    if response.status_code == 200:
        print(f'Sent DM to {username} using {account["username"]}: {generated_message}')
        return True
    else:
        print(f'Failed to send DM to {username} using {account["username"]}: {response.text}')
        return False

# Function to mark a username as "messaged" in the Google Sheets document
def mark_as_messaged(username):
    cell = worksheet.find(username)
    worksheet.update_cell(cell.row, cell.col + 1, 'Messaged')

# Function to iterate through and process usernames
def process_usernames():
    usernames = worksheet.col_values(1)  # Assuming usernames are in the first column
    account_index = 0  # Initialize to the first account

    for username in usernames:
        if username != '' and username != 'Messaged':
            account = instagram_accounts[account_index]
            if generate_and_send_dm(username, account):
                mark_as_messaged(username)
            time.sleep(60)  # Sleep to respect Instagram's rate limits

            # Switch to the next account in a round-robin manner
            account_index = (account_index + 1) % len(instagram_accounts)

if __name__ == '__main':
    process_usernames()