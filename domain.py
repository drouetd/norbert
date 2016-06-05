# -*- coding: utf-8 -*-

import os
import sys
import urllib
import requests
from urlparse import urlparse
from requests.auth import HTTPBasicAuth
from ConfigParser import SafeConfigParser
from utils import write_to_csv
from utils import generate_output_filename
from utils import dict_read_csv

def parse_args():
	file_name = raw_input("Path to CSV file to process: ")
	return file_name


def get_websites(records, fname, fields):
	""" 
	Iterate over list of contacts.Search Bing for company name \
	and add first result's URL to contact's record. """
	
	EXCLUDED = ('www.linkedin.com', 'www.facebook.com', 'www.wikipedia.org')
	augmented=[]
	
	for record in records:
		if record['company']:
			try:
				# get company URL
				result = bing_api(record['company'], top=1)
				if result['Url']:
					url = urlparse(result['Url'])
					if url.netloc not in EXCLUDED:
						record['website'] = url.netloc
					else:
						record['website'] = None
				else:
					record['website'] = None
				print record['website']
			except:
				# save work done so far and exit
				print "%s occurred processing %s." % (sys.exc_info()[0].__name__, record['contact'])
				#sys.exit()
		else:
			record['website'] = None
		augmented.append(record)
	
	return augmented


def bing_api(query, source_type = "Web", top = 10, format = 'json'):
	"""Returns the decoded json response content."""
	# Source --> https://xyang.me/using-bing-search-api-in-python/
	
	# get Bing API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_KEY = parser.get('bing', 'api_key')
	
	# set search url
	query = '%27' + urllib.quote(query) + '%27'
	# web result only base url
	base_url = 'https://api.datamarket.azure.com/Bing/SearchWeb/' + source_type
	url = base_url + '?Query=' + query + '&$top=' + str(top) + '&$format=' + format
	
	# create credential for authentication
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
	# create auth object
	auth = HTTPBasicAuth(API_KEY, API_KEY)
	# set headers
	headers = {'User-Agent': user_agent}
	
	# get response from search url
	response_data = requests.get(url, headers=headers, auth = auth)
	
	# decode json response content
	json_result = response_data.json()
	
	return json_result['d']['results'][0]


def main(filename):
	# parse input
	#filename = parse_args()
	output_filename = generate_output_filename(filename, "_web")
	headers = ['contact', 'company', 'title', 'city', 'province', 'country', 'website']
	
	# read data from csv
	employees = dict_read_csv(filename)
	
	# get website for companies
	augmented = get_websites(employees, filename, headers)	
	
	# write results to csv
	write_to_csv(output_filename, headers, augmented)
	
	# remove input file if op was succesful
	if os.path.exists(output_filename):
		os.remove(filename)
	
	return



if __name__ == "__main__":
	
	# parse input
	filename = parse_args()
	output_filename = generate_output_filename(filename, "_web")
	headers = ['contact', 'company', 'title', 'city', 'province', 'country', 'website']
	
	# read data from csv
	employees = dict_read_csv(filename)
	
	# get website for companies
	augmented = get_websites(employees, filename, headers)	
	
	# write results to csv
	write_to_csv(output_filename, headers, augmented)
	print "\nDone!"
