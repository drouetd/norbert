# -*- coding: utf-8 -*-

import sys
import csv
import requests

def read_csv(filename):
	""" Converts CSV file to list of dictionaries. """
	
	lst = []
	with open(filename, 'r') as f:
		csvfile = csv.reader(f)
		for row in csvfile:
			person = {}
			person['name'] = row[0]
			person['domain'] = row[1]
			lst.append(person)
	return lst

def post_norbert(payload, key):
	""" Posts to the voilanorbert.com api using the payload as parameters. """
	
	URL = "https://www.voilanorbert.com/api/v1/"
	add_credits = False
	payload['token'] = key
	
	# query the API
	try:
		r = requests.post(URL, data=payload)
		if r.status_code == 200:
			payload['success'] = r.json()['success']
			payload['emails'] = r.json()['emails']
			payload['error'] = None
		elif r.status_code == 410:
			payload['success'] = r.json()['success']
			payload['emails'] = None
			payload['error'] = r.json()['error']
			add_credits = True
		else:
			payload['success'] = r.json()['success']
			payload['emails'] = None
			payload['error'] = r.json()['error']
	except:
		print "%s occurred processing %s." % (sys.exc_info()[0].__name__, payload['name'])
		payload['success'] = None
		payload['emails'] = None
		payload['error'] = sys.exc_info()[0].__name__
	
	return payload, add_credits



if __name__ == '__main__':
	bulk = []
	# parse args and error handling
	
	# fetch the api key
	with open('Data/apikey.txt', 'r') as f:
		key = f.read()
	
	# load csv file with names to match
	bulk = read_csv('Data/test_error.csv')
	
	# send names norbert api one at a time
	for person in bulk:
		print "Payload sent: ", person
		result, buy_credits = post_norbert(person, key)
		print "result:", result
		print "buy_credits:", buy_credits
	
	# write results back to a csv
	
	# terminate with stats msg
	
	
	sys.exit()