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

	# Check if /stalked-profiles exists. If not, it will be created
	if os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__) ), 'stalked-profiles')) == False:
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'stalked-profiles')
		stalked_profiles = os.mkdir(path)
	else:
		stalked_profiles = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stalked-profiles') 

	# Check if /stalked-profiles/stalked_chiefs exists. If not, it will be created
	if os.path.isdir(os.path.join(stalked_profiles, 'stalked_chiefs')) == False:
		path = os.path.join(stalked_profiles,'stalked_chiefs')
		stalked_chiefs = os.mkdir(path)
	else:
		stalked_chiefs = os.path.join(stalked_profiles, 'stalked_chiefs')

	# Check if /stalked-profiles/stalked_economists exists. If not, it will be created
	if os.path.isdir(os.path.join(stalked_profiles, 'stalked_economists')) == False:
		path = os.path.join(stalked_profiles,'stalked_economists')
		stalked_economists = os.mkdir(path)
	else:
		stalked_economists = os.path.join(stalked_profiles, 'stalked_economists')

	# Get each file from /stalked_economists
	for filename in os.listdir(stalked_economists):
		if filename.endswith(".json"):
			logger.info("Reading {} file".format(filename))
			tweets = TweetsAnalysis().read_json(filename=os.path.join(stalked_economists, filename))
			TweetsAnalysis().db_complete(response=tweets, collection='economists')
		else:
			print("Only .json files are supported.")
			pass
	
	# Get each file from /stalked_chiefs
	for filename in os.listdir(stalked_chiefs):
		if filename.endswith(".json"):
			logger.info("Reading {} file".format(filename))
			tweets = TweetsAnalysis().read_json(filename=os.path.join(stalked_chiefs, filename))
			TweetsAnalysis().db_complete(response=tweets, collection='chiefs')
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

