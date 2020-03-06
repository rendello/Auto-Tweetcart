#!/usr/bin/python3.7

from pathlib import Path
from urllib3.exceptions import ProtocolError
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

        # https://developer.twitter.com/en/docs/basics/response-codes
        acceptable_errors = [
            44,  # Attachment url is invalid
            50,  # User not found
            63,  # User has been suspended
            88,  # Rate limit exceeded
            130,  # Twitter over capacity
            131,  # Internal error
            179,  # Not auth'd to see Tweet
            186,  # Tweet too long
            187,  # Tweet is duplicate
            385,  # Responding to deleted Tweet
            407,  # Invalid URL in Tweet
        ]
        try:
            # Grab 280 char "full" text, if it exists
            if not hasattr(status, "retweeted_status"):
                try:
                    text = status.extended_tweet["full_text"]
                except AttributeError:
                    text = status.text
            else:
                return

            text = html.unescape(text)
            text = remove_bot_call(text, bot_username)

            # Prevent infinite looping by bot
            if (f"@{status.author.screen_name}" == bot_username) and (
                "TEST" not in text
            ):
                return

            process_info = back_end.process_code(text)

            if process_info["was_successful"]:
                gif_id = api.media_upload("GIF/PICO-opti.gif").media_id

                if process_info["title"] == None:
                    tweet_text = f"#AutoTweetCart by @{status.author.screen_name}"
                else:
                    tweet_text = f"“{process_info['title']}” by @{status.author.screen_name}\n#AutoTweetCart"

                api.update_status(
                    tweet_text,
                    in_reply_to_status_id=status.id,
                    auto_populate_reply_metadata=True,
                    media_ids=[gif_id],
                )
        except tweepy.TweepError as error:
            print(f"{error.api_code}: {error.reason}")
            if error.api_code not in acceptable_errors:
                return

    def on_error(self, status_code):
        # True reconnects with a backoff, False ends the stream

        if status_code == 420:  # Too many attempts to connect to API
            print("Error 420: being rate-limited.")
            return True


key_file = Path("~/.autotweetcart/keys.json").expanduser()
with open(key_file, "r") as f:
    keys = json.load(f)

auth = authenticate(keys)
api = tweepy.API(auth)
bot_username = f"@{api.me().screen_name}"


stream = tweepy.Stream(auth=api.auth, listener=CartStreamListener())
stream.filter(track=[bot_username])
