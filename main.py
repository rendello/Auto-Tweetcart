#!/usr/bin/python3.7

from pathlib import Path
import json
import tweepy


def grab_keys(key_file):
    with open(key_file, "r") as tf:
        return json.load(tf)


def authenticate_new_user():
    """ Manually authenticate a new user account.
    """

    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    print(auth.get_authorization_url())

    verifier = input("Verifier: ")

    auth.request_token = {
        "oauth_token": auth.request_token["oauth_token"],
        "oauth_token_secret": verifier,
    }

    auth.get_access_token(verifier)
    print(f"acc token: {auth.access_token}")
    print(f"acc secret: {auth.access_token_secret}")


def authenticate(keys):
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_secret"])

    return auth


key_file = Path("~/.autotweetcart/keys.json").expanduser()
keys = grab_keys(key_file)
auth = authenticate(keys)
api = tweepy.API(auth)

user = api.me()
#print(user)


#override tweepy.StreamListener to add logic to on_status
class CartStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


stream = tweepy.Stream(auth=api.auth, listener=CartStreamListener())
stream.filter(track=['#tweetcart', '#tweetjam'])
