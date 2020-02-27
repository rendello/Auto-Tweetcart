#!/usr/bin/python3.7

from pathlib import Path
import json
import tweepy
import html

import back_end


def authenticate(keys):
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_secret"])

    return auth


def remove_bot_call(text, bot_username):
    new_text = ""
    for line in text.split("\n"):
        if bot_username not in line:
            new_text += f"{line}\n"
    return new_text


class CartStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        # --> Get text, regardless if retweet or not
        if hasattr(status, "retweeted_status"):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        # <--

        text = html.unescape(text)
        text = remove_bot_call(text, bot_username)

        # Prevent infinite looping by bot
        if (f"@{status.author.screen_name}" == bot_username) and ("TEST" not in text):
            return

        # Returns False if encounters profanity
        if back_end.process_code(text):
            gif_id = api.media_upload("GIF/PICO-opti.gif").media_id

            api.update_status(
                f"#AutoTweetCart by @{status.author.screen_name}",
                in_reply_to_status_id=status.id,
                auto_populate_reply_metadata=True,
                media_ids=[gif_id],
            )

    def on_error(self, status_code):
        if status_code == 420:  # Too many attempts to connect to API
            return True  # Reconnect w/ backoff


key_file = Path("~/.autotweetcart/keys.json").expanduser()
with open(key_file, "r") as f:
    keys = json.load(f)

auth = authenticate(keys)
api = tweepy.API(auth)
bot_username = f"@{api.me().screen_name}"

stream = tweepy.Stream(auth=api.auth, listener=CartStreamListener())
stream.filter(track=[bot_username])
