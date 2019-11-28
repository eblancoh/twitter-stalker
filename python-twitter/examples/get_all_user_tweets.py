#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Downloads all tweets from a given user.

Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
Twitter doesn't allow retreiving more tweets than this through the API, so we get
as many as possible.

t.py should contain the imported variables.
"""

from __future__ import print_function

import json
import sys
import shutil
import os
import twitter
from twitter.error import TwitterError
from t import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
    )
    ids = []
    with open('stalked.json', encoding="utf8") as json_file:
        json_data = json.load(json_file)
        for item in json_data['EquipoDirectivo']:
            if item["username"] != None:
                ids.append(item["username"])
         
    for screen_name in ids:
        try:
            timeline = get_tweets(api=api, screen_name=screen_name)
        except (TwitterError, ValueError) as e:
            pass

        with open(screen_name + '.json', 'w+') as f:
            for tweet in timeline:
                f.write(json.dumps(tweet._json))
                f.write('\n')
        
        basedir = os.path.dirname(os.path.realpath(__file__))
        grandpadir = os.path.dirname(os.path.dirname(basedir))

        # Los vamos moviendo a la carpeta que nos interesa (stalked meme)
        shutil.move(os.path.join(basedir, screen_name + '.json'), os.path.join(grandpadir, 'stalked-members', screen_name + '.json'))

        
        
    

    
