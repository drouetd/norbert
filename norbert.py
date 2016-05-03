# -*- coding: utf-8 -*-

import sys
import csv
import requests
from urlparse import urlparse


def extract_domain(website):
	domain = ''
	# urlparse only recognizes netloc if '//' present.
	if '//' not in website:
		website = '//' + website
	url = urlparse(website)
	parts = url.netloc.split('.')
	if len(parts) == 2:
		domain = url.netloc
	elif len(parts) > 2:
		domain = '.'.join(parts[-2:])
	else:
		print "Problem parsing %s." % website
	return domain


def read_csv(filename, name, website):
	""" Converts CSV file to list of dictionaries. """
	
	lst = []
	with open(filename, 'r') as f:
		csvfile = csv.reader(f)
		for row in csvfile:
			person = {}
			person['name'] = row[name]
			person['website'] = row[website]
			person['domain'] = extract_domain(row[website])
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
	if len(sys.argv) == 1:
		print "Usage: python norbert.py -i"
		sys.exit()
	elif sys.argv[1] == '-i':
		file_name = raw_input("Path to CSV file to process: ")
		col_name = raw_input("Column number that contains the person's name: ")
		col_website = raw_input("Column number that contains the company's website: ")
		# and because people don<t satrt counting at 0...
		col_name = int(col_name) - 1 
		if col_website != ('none' or 'None'):
			col_website = int(col_website) - 1
		else:
			col_website = None
	else:
		print "Error processing arguments."
		sys.exit()
			
	# fetch the api key
	with open('Data/apikey.txt', 'r') as f:
		key = f.read()
	
	# load csv file with names to match
	original = read_csv(file_name, col_name, col_website)
	
	# send names to the voilanorbert api one at a time
	for person in original:
		result, buy_credits = post_norbert(person, key)
		if buy_credits:
			# TODO:save names processed so far
			# mark where we are at
			# inform Dan that we need to buy more credits
			# exit with nice message
			print "Buy more credits!!!"
			sys.exit()
		else:
			augmented.append(result)
	
	# write augmented list to a csv
	output_filename = "Data/out.csv"
	fields = ['name', 'website', 'domain', 'success', 'emails', 'error']
	write_to_csv(output_filename, fields, augmented)
	
	# terminate with stats msg
	processed = len(original)
	matched = len([person for person in original if person['success']==True])
	print "\nNames processed: %d" % processed
	print "Names matched to emails: %d" % matched
	if processed:
		percent = (matched / float(processed))*100
		print "Success rate: %.1f percent" % percent
	else:
		print "Success rate: n/a"
	print "Done!"
	
	sys.exit()