import requests
import socket
import json
import numpy as np
from urllib.parse import urlparse
import configparser
import pymongo
import sys
import argparse
import time
import datetime
import time

config = configparser.ConfigParser()
config.read("config.ini")

user = config['mongodb']['user']
password = config['mongodb']['passwd']
db_name = config['mongodb']['database']

client = pymongo.MongoClient("mongodb+srv://" + user + ":" + password + "@" + db_name + "-mxffd.mongodb.net/test?retryWrites=true&w=majority")
db = client.twitter

collection_stalker = db.stalkercollection
collection_economists = db.economistscollection
collection_recomendations = db.recomendationscollection

records = dict()

dt = datetime.datetime.now()
day = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
ts = str(dt.hour) + ':' + str(dt.minute)

records['day'] = day
records['ts'] = ts
records['stalker'] = collection_stalker.count()
records['economists'] = collection_economists.count()
records['recomendations'] = collection_recomendations.count()

with open('records.json', 'a+') as f:
    f.write(json.dumps(records))
    f.write('\n')
