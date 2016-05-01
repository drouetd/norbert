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


def write_to_csv(filename, fields, records):
	""" Writes a list of dictionaries to a csv file. """
	
	with open(filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
		# writer.writeheader()
		for rec in records:
			try:
				writer.writerow(rec)
			except:
				print "%s occurred with %s" % (sys.exc_info()[0].__name__, rec[fields[0]])
				print rec
				print'\n'
	return 


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
	
	# remove API key before returning
	del payload['token']
	
	return payload, add_credits



if __name__ == '__main__':
	original = []
	augmented = []
	# parse args and error handling
	
	# fetch the api key
	with open('Data/apikey.txt', 'r') as f:
		key = f.read()
	
	# load csv file with names to match
	original = read_csv('Data/test.csv')
	
	# send names to the voilanorbert api one at a time
	for person in original:
		result, buy_credits = post_norbert(person, key)
		if buy_credits:
			# save names processed so far
			# mark where we are at
			# inform Dan that we need to buy more credits
			# exit with nice message
			pass
		else:
			augmented.append(result)
	
	# write augmented list to a csv
	output_filename = "Data/test1_out.csv"
	fields = ['name', 'domain', 'success', 'emails', 'error']
	write_to_csv(output_filename, fields, augmented)
	
	# terminate with stats msg
	print "\nDone!"
	
	sys.exit()