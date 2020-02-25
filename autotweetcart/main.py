#!/usr/bin/python3.7

from pathlib import Path
import json
import tweepy
import pico8
import html


def grab_keys(key_file):
    with open(key_file, "r") as tf:
        return json.load(tf)


def authenticate(keys):
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_secret"])

    return auth


# override tweepy.StreamListener to add logic to on_status
class CartStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        text = html.unescape(text)

        if (status.author.screen_name == "auto_tweetcart") and ("TEST" not in text):
            # Prevent infinite looping by bot
            return

        # Returns False if encounters curses
        if pico8.process_code(text):
            gif_id = api.media_upload("GIF/PICO-opti.gif").media_id

            api.update_status(
                f"#AutoTweetCart by @{status.author.screen_name}", in_reply_to_status_id=status.id, auto_populate_reply_metadata=True, media_ids=[gif_id]
            )

    def on_error(self, status_code):
        if status_code == 420:  # Too many attempts to connect to API
            return True  # Reconnect w/ backoff


key_file = Path("~/.autotweetcart/keys.json").expanduser()
keys = grab_keys(key_file)
auth = authenticate(keys)
api = tweepy.API(auth)

stream = tweepy.Stream(auth=api.auth, listener=CartStreamListener())
stream.filter(
    track=[
        "@auto_tweetcart",
    ]
)
