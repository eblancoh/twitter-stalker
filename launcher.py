from engine import TweetsAnalysis
import configparser
import schedule
import time
import sys
import json
import os
from requests import get
from watcher import get_logger

# # Activity logging definition
logger = get_logger('__main__')

# Configuration loading
config = configparser.ConfigParser()
config.read("config.ini")
# Get the filtered ips to CRUD in MongoDB Database
filtered_ips = dict(config.items('ipwhitelist'))

def get_IP(): 
	#https://www.ipify.org/
	ip = get('https://api.ipify.org').text 
	return ip


def main():

	# Leer secuencialmente de la carpea stalked-members
	# json files directory of memebers of the boards
	stalked_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stalked-members')

	for filename in os.listdir(stalked_directory):
		if filename.endswith(".json"):
			logger.info("Reading {} file".format(filename))
			tweets = TweetsAnalysis().read_json(filename=os.path.join(stalked_directory, filename))
			TweetsAnalysis().db_complete(response=tweets)
		else:
			print("Only .json files are supported.")
			pass

	logger.info("Finished batch of queries...")


if __name__=='__main__':
	# Obtain my_ip
	my_ip=get_IP()

	# Check that we're going out a certain filtered IP by the database
	if my_ip in filtered_ips.values():
		# Schedule routine with certain frequency
		schedule.every(1).minutes.do(main)
		# schedule.every().hour.do(main)
		# schedule.every().day.at("12:00").do(main)
		while True:
			try:
				schedule.run_pending()
				time.sleep(1)
			except KeyboardInterrupt:
				sys.exit('Ctrl+c - Routine stopped by user.')
	
	else:
		logger.error("IP address not included in database filtered addresses.")
		sys.exit('Connect to a network with granted access to the database.')

