# -*- coding: utf-8 -*-

import sys
import time
import requests
from ConfigParser import SafeConfigParser
import pprint


def norbert_post(name, domain):
	
	# get Voilanorbert API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_TOKEN = parser.get('norbert', 'api_token')
	
	POST_URL = "https://api.voilanorbert.com/2016-01-04/search/name"
	headers = {'api-token': API_TOKEN}
	payload = {'name': name, 'domain': domain}
	email = None
	
	r = requests.post(POST_URL, headers=headers, data=payload)
	
	print "\nPOST"
	print "response code: ", r.status_code
	print "json: ", r.json()
	
	if r.status_code == 200:
		ident = r.json()['id']
		if not r.json()['searching']:
			#print r.json()
			if r.json()['email']:
				# email found
				email = r.json()['email']['email']
			else:
				# email not found
				pass
	else:
		# there was a problem"
		ident = -1
	
	return ident, email, r.status_code


def norbert_get(person_id):
	
	# get Voilanorbert API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_TOKEN = parser.get('norbert', 'api_token')
	
	GET_URL = "https://api.voilanorbert.com/2016-01-04/contacts/"
	headers = {'api-token': API_TOKEN}
	payload = {'id': person_id }
	email = None
	abort = False # hack because the GET sometimes can't find the post'ed ID which raises a StopIteration exception.
	
	r = requests.get(GET_URL, headers=headers, params=payload)
	
	print "\nGET"
	print "response code: ", r.status_code
	records = r.json()['result']
	pprint.pprint(records)
	
	# is Norbert still searching for the email addr?
	try:
		record = (rec for rec in records if rec['id']==person_id).next()
	except:
		print "GET: couldn't find ID: %d" % person_id
		# give up on this one
		abort = True
		return False, email, abort
	if not record['searching']:
		# search finished
		print record
		if record['email']:
			# email found
			email = record['email']['email']
		else:
			# email not found
			pass
	
	return record['searching'], email, abort


def find_email(name, domain):
	
	email = None
	
	# initial query
	id_no, email, status_code = norbert_post(name, domain)
	if status_code == 200:
		# result of query
		if email:
			pass
		else:
			# poll until search completes
			searching = True
			count = 0
			while searching and count < 30:
				time.sleep(2)
				searching, email, abort = norbert_get(id_no)
				if abort:
					print "Aborting."
					break
				count += 2
	
	return email, status_code

	