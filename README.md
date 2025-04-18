# Reddit-to-Bluesky
- Copy top post of the day from a subreddit to a Bluesky Account. Lots of nonsense in here to account for links and their version of hashtags.

# Setup

## Setup a Linux Host
I'm using Ubuntu LTS on an Oracle Cloud VM. There are free-tiers available as of today. Google Compute and Amazon AWS are similar products. You can also roll your own host with an old PC or a Raspberry Pi. You'll need to know a bit of Linux CLI or you'll need to be ready to learn! Run these commands through the CLI.

## Setup Git
1. [Create a Github account.](https://github.com/join)

2. [Go here and install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you don’t have it already.

3. [Assuming you're reading this on the repo page](https://github.com/SaltySOMAdmin/Reddit-to-Bluesky), select ‘fork’ to create a copy of it to your Github account. 

4. From your new repo, select **Code** and then under **Clone** copy the HTTPS URL (e.g. https://github.com/SaltySOMAdmin/Reddit-to-Bluesky.git) to download a local copy

5. Navigate to a folder you want a local copy of the repo to live, and clone the Github repo to your host:
   1. It's up to you where to put the repo - recommended in a folder like /home/YourUserAcct/Github/ or /home/YourUserAcct/. Once you clone the directory it will create a subfolder with the name of your fork.
   2. git clone `<url>`
      1. e.g. git clone https://github.com/SaltySOMAdmin/Reddit-to-Bluesky.git


## Install necessary software prerequisites: 
1. Install Python3

		sudo apt install python3

2. Create a python virtual environment in a directory

		/usr/bin/python3 -m venv /home/ubuntu/Reddit-to-Bluesky/

3. Use the virtual python3 environment

		source /home/ubuntu/Reddit-to-Bluesky/bin/activate

4. Install Bluesky SDK and other pre-reqs

		pip install atproto
	
		pip install praw

## Configure the script.

1. Create a file called config.py and save it in the same directory as your script. Enter Reddit and Twitter api credentials. Check out the example file for formatting. 

2. Configure forward_log.sh with a Discord webhook if you want logs forwarded. Enter the webhook in a .txt in the same directory or directly into the code. 
	
3. Setup a schedule to run

		crontab -e 
	
		#Bluesky Post daily at noon
	
		0 17 * * * /bin/bash -c "source /home/ubuntu/Reddit-to-Bluesky/bin/activate && python3 /home/ubuntu/Reddit-to-Bluesky/topPostDay.py" >> /home/ubuntu/Reddit-to-Bluesky/bluesky_log.txt 2>&1 
	
		#upload logs to Discord
	
		5 17 * * * /home/ubuntu/Reddit-to-Bluesky/forward_log.sh
	
## Setup Continuous Deployment with Github Actions

Allows you to deploy your code via Github vs logging into the VPS and updating the code/uploading a new file. Allows for easier collaboration as well. I followed a guide similar to this one:
https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-with-github-actions
	
