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
