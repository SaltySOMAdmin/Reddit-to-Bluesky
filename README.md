# Reddit-to-Bluesky-Public
 
Copy top post of the day from a subreddit to a bluesky account. 

1) Install Python3

	sudo apt install python3

2) Create a python virtual environment in a directory

	/usr/bin/python3 -m venv /home/ubuntu/bluesky/

3) Use the virtual python3 environment

	source /home/ubuntu/bluesky/bin/activate

4) Install Bluesky SDK and other pre-reqs

	pip install atproto
	
	pip install praw

5) Create a file called config.py and save it in the same directory as your script. Enter Reddit and BlueSky api credentials.

6) Configure forward_log.sh with a discord webhook if you want logs forwarded. 
	
7) Setup a schedule to run

	crontab -e 
	
	#BlueSky Post daily at noon
	
	0 17 * * * /bin/bash -c "source /home/ubuntu/bluesky/bin/activate && python3 /home/ubuntu/bluesky/topPostDay.py" >> /home/ubuntu/bluesky/log.txt 2>&1
	
	#upload BlueSky logs
	
	5 17 * * * /home/ubuntu/bluesky/forward_log.sh
	
	
