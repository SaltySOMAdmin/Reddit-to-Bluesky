# Reddit-to-Bluesky
 
Copy top post of the day from a subreddit to a bluesky account. 

1) Install Python3
   
	sudo apt install python3

3) Create a python virtual environment in a directory
   
	/usr/bin/python3 -m venv /home/ubuntu/bluesky/

4) Use the virtual python3 environment
   
	source /home/ubuntu/bluesky/bin/activate

5) Install Bluesky SDK and other pre-reqs
   
	pip install atproto
	pip install praw

6) Create a file called config.py and save it in the same directory as your script. Enter Reddit and BlueSky api credentials.

7) Configure forward_log.sh with a discord webhook if you want logs forwarded. 
	
8) Setup a schedule to run
   
	crontab -e 
	#BlueSky Post daily at noon
	0 17 * * * /bin/bash -c "source /home/ubuntu/bluesky/bin/activate && python3 /home/ubuntu/bluesky/topPostDay.py" >> /home/ubuntu/bluesky/log.txt 2>&1
	#upload BlueSky logs
	5 17 * * * /home/ubuntu/bluesky/forward_log.sh
	
