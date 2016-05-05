# -*- coding: utf-8 -*-

import sys
import csv
import time
import urllib
import requests
from requests.auth import HTTPBasicAuth
from googlesearch import GoogleSearch
from norbert import write_to_csv
from norbert import generate_output_filename

def parse_args():
	# parse args and error handling
	if len(sys.argv) == 1:
		print "Usage: python norbert.py -i"
		sys.exit()
	elif sys.argv[1] == '-i':
		file_name = raw_input("Path to CSV file to process: ")
		col_name = raw_input("Column number that contains the person's name: ")
		col_company = raw_input("Column number that contains the company name: ")
		# and because people don't start counting at 0...
		col_name = int(col_name) - 1 
		if col_company != ('none' or 'None'):
			col_company = int(col_company) - 1
		else:
			col_company = None
	else:
		print "Error processing arguments."
		sys.exit()
	return file_name, col_name, col_company


def read_csv(filename, name, company):
	""" Converts CSV file to list of dictionaries. """
	
	lst = []
	with open(filename, 'r') as f:
		csvfile = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
		for row in csvfile:
			person = {}
			person['name'] = row[name]
			person['company'] = row[company]
			lst.append(person)
	return lst


def get_website(company_name):
	#gs = GoogleSearch(company_name)
	results = bing_api(company_name, top=1)
	#for results in results:
	print "\n%s" % company_name
	print results['Url']
	print results['Description']
	return results['Url']


def google_search(query):
	URL = "https://ajax.googleapis.com/ajax/services/search/web"
	params = {'v':1.0, 'q': query}
	r = requests.get(URl, data=params)


def bing_api(query, source_type = "Web", top = 10, format = 'json'):
	"""Returns the decoded json response content."""
	# Source --> https://xyang.me/using-bing-search-api-in-python/
	
	# Bing API key
	API_KEY = "tDG6GvbiMPX2kxr9PQHF8OSKtnstlm8StD91YR3lE/8"
	
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
	
	# parse input and format output
	filename, person_name, company_name = parse_args()
	output_filename = generate_output_filename(filename, "_web")
	output_fields = ['name', 'company', 'website']
	
	# read data from csv
	employees = read_csv(filename, person_name, company_name)
	
	# get website for companies
	results = []
	for employee in employees:
		try:
			employee['website'] = get_website(employee['company'])
		except:
			# save work done so far and exit
			write_to_csv(output_filename, output_fields, results)
			print "%s occurred processing %s." % (sys.exc_info()[0].__name__, employee['name'])
			sys.exit()
		print employee['website']
		results.append(employee)
		#time.sleep(15)
	
	# write results to csv
	write_to_csv(output_filename, output_fields, results)
	print "\nDone!"
