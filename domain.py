# -*- coding: utf-8 -*-

import sys
import urllib
import requests
from requests.auth import HTTPBasicAuth
from ConfigParser import SafeConfigParser
from formatting import write_to_csv
from formatting import generate_output_filename
from formatting import dict_read_csv

def parse_args():
	file_name = raw_input("Path to CSV file to process: ")
	return file_name


def get_websites(records):
	""" Iterate over list of contacts.Search Bing for company name \
		and add first result's URL to contact's record. """
	
	augmented=[]
	for record in records:
		try:
			# get company URL
			result = bing_api(record['company'], top=1)
			record['website'] = result['Url']
		except:
			# save work done so far and exit
			write_to_csv(output_filename, output_fields, results)
			print "%s occurred processing %s." % (sys.exc_info()[0].__name__, record['contact'])
			sys.exit()
		print record['website']
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




if __name__ == "__main__":
	
	# parse input
	filename = parse_args()
	output_filename = generate_output_filename(filename, "_web")
	
	# read data from csv
	employees = dict_read_csv(filename)
	
	# get website for companies
	augmented = get_websites(employees)	
	
	# write results to csv
	headers = ['contact', 'company', 'website']
	write_to_csv(output_filename, headers, augmented)
	print "\nDone!"
