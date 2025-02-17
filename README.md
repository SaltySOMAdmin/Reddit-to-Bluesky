# Reddit-to-Bluesky
 
 
## Copy top post of the day from a subreddit to a Bluesky Account. Lots of nonsense in here to account for links and their version of hashtags.

### 1) Install Python3

	sudo apt install python3

### 2) Create a python virtual environment in a directory

	/usr/bin/python3 -m venv /home/ubuntu/Reddit-to-Bluesky/

### 3) Use the virtual python3 environment

	source /home/ubuntu/Reddit-to-Bluesky/bin/activate

### 4) Install Bluesky SDK and other pre-reqs

	pip install atproto
	
	pip install praw

### 5) Create a file called config.py and save it in the same directory as your script. Enter Reddit and Twitter api credentials.

### 6) Configure forward_log.sh with a discord webhook if you want logs forwarded. Enter the webhook in a .txt in the same directory or directly into the code. 
	
### 7) Setup a schedule to run

crontab -e 
	
	#Bluesky Post daily at noon
	
	0 17 * * * /bin/bash -c "source /home/ubuntu/Reddit-to-Bluesky/bin/activate && python3 /home/ubuntu/Reddit-to-Bluesky/topPostDay.py" >> /home/ubuntu/Reddit-to-Bluesky/bluesky_log.txt 2>&1 
	
	#upload logs to Discord
	
	5 17 * * * /home/ubuntu/Reddit-to-Bluesky/forward_log.sh
	
	
