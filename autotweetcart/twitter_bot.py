#!/usr/bin/python3.7

from pathlib import Path
from urllib3.exceptions import ProtocolError
import json
import tweepy
import html
import sys

import back_end
from simple_logging import log


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
            # ===== Grab tweet text; ignore retweets
            if not hasattr(status, "retweeted_status"):
                try:
                    text = status.extended_tweet["full_text"]
                except AttributeError:
                    text = status.text
            else:
                log("Ignoring Retweet.")
                return

            log(f"Status found: <{status.id}> {text}")

            text = html.unescape(text)
            text = remove_bot_call(text, bot_username)

            # ===== Ignore bot's own Tweets
            if (f"@{status.author.screen_name}" == bot_username) and (
                "TEST" not in text
            ):
                log("Ignoring own Tweet.")
                return

            # ===== Pass text off to back end
            log("Processing Tweet.")
            process_info = back_end.process_code(text)

            if process_info["was_successful"]:
                gif_id = api.media_upload("GIF/PICO-opti.gif").media_id

                # ===== Upload result GIF
                if process_info["title"] == None:
                    tweet_text = f"#AutoTweetCart by @{status.author.screen_name}"
                else:
                    tweet_text = f"“{process_info['title']}” by @{status.author.screen_name}\n#AutoTweetCart"

                reply_status = api.update_status(
                    tweet_text,
                    in_reply_to_status_id=status.id,
                    auto_populate_reply_metadata=True,
                    media_ids=[gif_id],
                )
                log(f"Posted tweet: <{reply_status.id}> {tweet_text}")
            else:
                log("Processing failed.")

        except tweepy.TweepError as error:
            log(f"{error.api_code}: {error.reason}")
            if error.api_code not in acceptable_errors:
                return

    def on_error(self, status_code):
        # True reconnects with a backoff, False ends the stream

        if status_code == 420:  # Too many attempts to connect to API
            log("Error 420: being rate-limited.")
            return True


if __name__ == "__main__":
    key_file = Path("~/.autotweetcart/keys.json").expanduser()

    with open(key_file, "r") as f:
        keys = json.load(f)

    auth = authenticate(keys)
    api = tweepy.API(auth)
    bot_username = f"@{api.me().screen_name}"

    stream = tweepy.Stream(auth=api.auth, listener=CartStreamListener())

    try:
        log("===== Starting =====")
        stream.filter(track=[bot_username])
    except KeyboardInterrupt as e:
        log("Keyboard interrupt. Closing.")
        sys.exit(0)
