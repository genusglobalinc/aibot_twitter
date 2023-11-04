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

follow these instructions:
1. Buy 10 aged instagram accounts
2. Setup api access keys for accounts
3. store account information in accessible google sheets doc
4. create a dialogflow agent and define intents and webhooks
5. create google sheets to store prospects 
6. copy python script to EC2 instance 
7. create control_panel.html template on EC2 instance
8. set variables for one test cycle (4000dms run once)
9. launch bot on server by running script from EC2 instance
10. control bot from web interface 