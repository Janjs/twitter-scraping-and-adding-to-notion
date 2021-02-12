import tweepy
from tweepy import OAuthHandler
from notion.client import NotionClient
from notion.block import ImageBlock
import pandas as pd
from PIL import Image
import requests
import time

access_token = '############'
access_token_secret = '############'
consumer_key = '############'
consumer_secret = '############'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = api.user_timeline(screen_name='wsbmod',
                           count=20,
                           include_rts=False,
                           tweet_mode='extended'
                           )

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
token_v2 = "'############'"
client = NotionClient(token_v2)
# Replace this URL with the URL of the page you want to edit
page = client.get_block('https://www.notion.so/your-url')

for tweet in tweets:
    if "Most discussed stocks for" in tweet.full_text:
        print(tweet.full_text)
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                imageBlock = page.children.add_new(
                    ImageBlock, title=tweet.full_text, width=500)
                # sets "property.source" to the URL, and "format.display_source" to the embedly-converted URL
                imageBlock.set_source_url(image['media_url'])
