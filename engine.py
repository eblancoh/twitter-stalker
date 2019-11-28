import requests
import socket
import json
import numpy as np
from urllib.parse import urlparse
import configparser
import pymongo
import sys
import argparse
from watcher import get_logger
from textanalytics import language, sentiments, keyPhrases, entities

config = configparser.ConfigParser()
config.read("config.ini")

logger = get_logger('engine')

class TweetsAnalysis(object):

	def read_json(self, filename):
		data = list()
		self.filename = filename
		with open(filename) as f:
			for line in f:
				data.append(json.loads(line))
		return data
	
	@staticmethod
	def db_complete(response, collection):
		# Nos conectamos a la base de datos en mongodb atlas
		# client = pymongo.MongoClient("mongodb+srv://holygrail:<password>@database-mxffd.mongodb.net/test?retryWrites=true&w=majority")
		user = config['mongodb']['user']
		password = config['mongodb']['passwd']
		db_name = config['mongodb']['database']

		client = pymongo.MongoClient("mongodb+srv://" + user + ":" + password + "@" + db_name + "-mxffd.mongodb.net/test?retryWrites=true&w=majority")
		db = client.twitter
		collection_stalker = db.stalkercollection
		collection_economists = db.economistscollection

		# insertamos el contenido de las noticias como documentos en la colección
		# Lo que nos interesa está almacenado en "value"
		try:
			for j in response:
				# To check if a certain entrance already exists in database
				# to avoid duplications in our collection
				if collection == 'chiefs':
					if collection_stalker.find({'id': j['id']}).count() == 0:
						# Incorporamos el lenguaje detectado
						j['detectedLanguages'] = language(j)
						# Detectamos sentimiento
						j['sentiment'] = sentiments(j)
						# Almacenamos las keyPhrases
						j['keyPhrases'] = keyPhrases(j)
						# Almacenamos las entities
						j['entities'] = entities(j)
						post_id = collection_stalker.insert_one(j).inserted_id
						logger.info("_id {} document inserted in database [Collection {}]".format(post_id, collection))
					else:
						pass
				else:
					if collection_economists.find({'id': j['id']}).count() == 0:
						# Incorporamos el lenguaje detectado
						j['detectedLanguages'] = language(j)
						# Detectamos sentimiento
						j['sentiment'] = sentiments(j)
						# Almacenamos las keyPhrases
						j['keyPhrases'] = keyPhrases(j)
						# Almacenamos las entities
						j['entities'] = entities(j)
						post_id = collection_economists.insert_one(j).inserted_id
						logger.info("_id {} document inserted in database [Collection {}]".format(post_id, collection))
					else:
						pass
		except KeyError:
			logger.warning("Something went wrong :P")
			pass


	