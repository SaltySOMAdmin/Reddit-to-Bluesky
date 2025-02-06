import logging
import praw
from atproto import Client
import datetime
import warnings
import re
from typing import List, Dict
import requests
import config  # Import the config file with credentials

# Configure logging
logging.basicConfig(
    filename="/home/ubuntu/bluesky/log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

warnings.filterwarnings("ignore", category=SyntaxWarning)

# Function to parse mentions
def parse_mentions(text: str) -> List[Dict]:
    spans = []
    mention_regex = rb"[$|\W](@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(mention_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "handle": m.group(1)[1:].decode("UTF-8")
        })
    return spans

# Function to parse URLs
def parse_urls(text: str) -> List[Dict]:
    spans = []
    url_regex = rb"[$|\W](https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*[-a-zA-Z0-9@%_\+~#//=])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(url_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "url": m.group(1).decode("UTF-8"),
        })
    return spans

# Function to parse hashtags
def parse_hashtags(text: str) -> List[Dict]:
    spans = []
    hashtag_regex = rb"(#\w+)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(hashtag_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "hashtag": m.group(1).decode("UTF-8"),
        })
    return spans

# Function to parse facets from text
def parse_facets(text: str) -> List[Dict]:
    facets = []
    for m in parse_mentions(text):
        resp = requests.get(
            "https://bsky.social/xrpc/com.atproto.identity.resolveHandle",
            params={"handle": m["handle"]},
        )
        if resp.status_code == 400:
            continue
        did = resp.json()["did"]
        facets.append({
            "index": {
                "byteStart": m["start"],
                "byteEnd": m["end"],
            },
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}],
        })
    for u in parse_urls(text):
        facets.append({
            "index": {
                "byteStart": u["start"],
                "byteEnd": u["end"],
            },
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#link",
                    "uri": u["url"],
                }
            ],
        })
    for h in parse_hashtags(text):
        facets.append({
            "index": {
                "byteStart": h["start"],
                "byteEnd": h["end"],
            },
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": h["hashtag"]}],
        })
    return facets

# Reddit API credentials from config
reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT
)

# BlueSky API credentials from config
bsky_username = config.BSKY_USERNAME
bsky_password = config.BSKY_PASSWORD

# Initialize BlueSky client
bsky = Client()
try:
    bsky.login(bsky_username, bsky_password)
    logging.info("Logged in to BlueSky successfully!")
except Exception as e:
    logging.error(f"Failed to log in to BlueSky: {e}")
    exit()

# Fetch the top post from the last day from r/ufos
subreddit = reddit.subreddit('ufos')
top_posts = subreddit.top(time_filter='day', limit=1)

for post in top_posts:
    post_title = post.title 
    post_url = f"https://reddit.com{post.permalink}"
    post_score = post.score

    skeet_content = f"Top post from r/UFOs in the last day. #UFOSky:\n\n{post_title}\nScore: {post_score}\n{post_url} #UFOs #UAP "

    if len(skeet_content) > 300:
        truncated_title = post_title[:(300 - len(skeet_content)) + 20] + "..."
        skeet_content = f"Top post from r/UFOs in the last day. #UFOSky:\n\n{truncated_title}\n{post_url}"
    
    facets = parse_facets(skeet_content)
    
    try:
        bsky.send_post(skeet_content, facets=facets)
        logging.info("Skeet posted successfully!")
        logging.info(skeet_content)
    except Exception as e:
        logging.error(f"Error posting to BlueSky: {e}")

    break
