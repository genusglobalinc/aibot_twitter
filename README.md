# aibot_twitter

To connect AWS console where code is launched

Instance ID
i-02874aa4d55110595
Open an SSH client.

Locate your private key file. The key used to launch this instance is aibot_twitter_kp.pem

Run this command, if necessary, to ensure your key is not publicly viewable.
 chmod 400 aibot_twitter_kp.pem

Connect to your instance using its Public DNS:
 ec2-13-59-67-53.us-east-2.compute.amazonaws.com

Example:

 ssh -i "aibot_twitter_kp.pem" ubuntu@ec2-13-59-67-53.us-east-2.compute.amazonaws.com

 You might have to use wget to get the file.
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID' -O FILE_NAME


IMPORTANT!!!!
To use this code, aibot_instagram-v4.py is the working rendition. 

Follow these instructions:
1. Buy 10 aged instagram accounts
2. Setup api access keys for accounts
   -download .json creds file to google drive
   
4. store account information in accessible google sheets doc
   -create google doc sheet
   
5. create a dialogflow agent and define intents and webhooks
6. copy python script to EC2 instance and set up environment
   -cd to directory
   -gpg --gen-key (create username and password)
   -
   -wget your .json file to your local directory to your saved google file creds
   -git pull https://github.com/genusglobalinc/aibot_twitter (clone for later edits)
   -edit api keys and access tokens for ig account(s), residential proxy service, and OpenAI, 
   -define hashtags, set Google Sheets name, and set desired prospecting limit

8. create control_panel.html template on EC2 instance
9. set variables for one test cycle (4000dms run once)
10. launch bot on server by running script from EC2 instance
11. control bot from web interface 
