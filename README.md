# aibot_twitter

To connect AWS console where code is hosted on Flask server
Open an SSH client.

Locate your private key file. The key used to launch this instance is aibot_twitter_kp.pem

Run this command, if necessary, to ensure your key is not publicly viewable:
chmod 400 aibot_twitter_kp.pem

Connect to your instance using its Public DNS:
ec2-13-59-67-53.us-east-2.compute.amazonaws.com

Example:

 ssh -i "aibot_twitter_kp.pem" ubuntu@ec2-13-59-67-53.us-east-2.compute.amazonaws.com

You might have to use wget to get the file:
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID' -O FILE_NAME


IMPORTANT!!!!
To properly install code, aibot_instagram-v4.py is the working rendition. 

Follow these instructions:
1. Buy 10 aged instagram accounts
2. Setup api access keys for accounts
   -download .json creds file to google drive to be accessed with wget later

   -enable DialogFlow api in Cloud Console: https://console.cloud.google.com/

   To enable the Dialogflow API:

   In the Cloud Console, navigate to the "APIs & Services" > "Dashboard" page.
   Click on "+ ENABLE APIS AND SERVICES."
   Search for "Dialogflow API" and enable it.
   Create a Service Account:
   
   In the Cloud Console, navigate to the "APIs & Services" > "Credentials" page.
   Click on "Create Credentials" and choose "Service account key."
   Select or create a service account, choose a role (Dialogflow API Client would typically suffice), and choose JSON as the key type.
   Click "Create" to download the JSON key file.
   Set Environment Variable in Your Code:
   
   Upload the downloaded JSON key file to a location accessible to your code, for example, on your server or in your code repository.
   Set the DIALOGFLOW_KEY_FILE variable in your Python code to the path of this file.

   Final command to run: wget --no-check-certificate "https://drive.google.com/file/d/1bAp_NapZjOkt0ZMkM_xRw3QEs7em6bRu/view?usp=drive_link" -O dialogflow_apiclient.json
   
4. store account information in accessible google sheets doc
   -create google doc sheet
   
5. create a dialogflow agent and define intents and webhooks on DialogFlow web console
   -create intent called "BookMeeting"

   -activate and create webhook, using "<Copy and paste your full Public IPv4 DNS here>" + "/dialogflow-webhook" as the fulfillment URL

   -add training phrases to indicate interest in booking a meeting

   -create any needed intents, and edit code accordingly
   
6. copy python script to EC2 instance and set up environment
   -cd to directory

   -gpg --gen-key (create username and password)

   -wget --no-check-certificate 'https://drive.google.com/file/d/1VMZvgLzGTTrzKUbQ--34WYvzCpEp9dad/view?usp=sharing' -O googlejson.json

   -git pull https://github.com/genusglobalinc/aibot_twitter (clone for later edits)

   -edit api keys and access tokens for ig account(s), residential proxy service, and OpenAI, 

   -define hashtags, set Google Sheets name, and set desired prospecting limit

9. create control_panel.html template on EC2 instance

10. set variables for one test cycle (4000dms run once)

11. launch bot on server by running script from EC2 instance

12. control bot from web interface: http://ec2-13-59-67-53.us-east-2.compute.amazonaws.com:5000


ACCESSING EC2 INSTANCE USING AWS MOBILE CLOUDSHELL CONSOLE:
1. wget --no-check-certificate 'https://drive.google.com/file/d/1oZZ_guVtdaMHso89l-YBFZPM7FjhTGoA/view?usp=sharing' -O aibot_twitter_kp.pem
2. OPTIONAL: upload file to cloudshell console
3. ssh -i "aibot_twitter_kp.pem" ec2-user@ec2-13-59-67-53.us-east-2.compute.amazonaws.com

