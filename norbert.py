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

def post_norbert(payload):
	""" Posts to the voilanorbert.com api using the payload as parameters. """
	
	URL = "https://www.voilanorbert.com/api/v1/"
	
	# read the API key from a file that's not available on public GitHub repo :-)
	with open('Data/apikey.txt', 'r') as f:
		key = f.read()
	
	# query the API
	payload['token'] = key
	r = requests.post(URL, data=payload)
	print "status code:", r.status_code
	print "headers:", r.headers
	print "test:", r.text
	print "json:", r.json()
	print
	
	return



if __name__ == '__main__':
	bulk = []
	# parse args and error handling
	
	# load csv file with names to match
	bulk = read_csv('Data/test1.csv')
	for person in bulk:
		print person
	
	# send names norbert api one at a time
	for person in bulk:
		print "Payload sent: ", person
		post_norbert(person)
	
	# write results back to a csv
	
	# terminate with stats msg
	
	
	sys.exit()