# -*- coding: utf-8 -*-

import sys
import time
import requests
from ConfigParser import SafeConfigParser

def norbert1(name, domain):
	""" Posts to the voilanorbert.com api using the payload as parameters. """
	
	# get Voilanorbert API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_KEY = parser.get('norbert_v1', 'api_key')
	
	URL = "https://www.voilanorbert.com/api/v1/"
	add_credits = False
	payload = {'token': API_KEY, 'name': name, 'domain': domain}
	email = ''
	
	# query the API
	try:
		r = requests.post(URL, data=payload)
		if r.status_code == 200:
			# extract email from list of emails
			email_list = r.json()['emails']
			for mail in email_list:
				email += mail
				email += ' ,'
			email = email.rstrip(',')
			#email = r.json()['emails']
	except:
		print "%s occurred processing %s." % (sys.exc_info()[0].__name__, payload['name'])
	
	return email, r.status_code


def norbert2_post(name, domain):
	
	# get Voilanorbert API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_TOKEN = parser.get('norbert_v2', 'api_token')
	
	POST_URL = "https://api.voilanorbert.com/2016-01-04/search/name"
	headers = {'api-token': API_TOKEN}
	payload = {'name': name, 'domain': domain}
	email = None
	
	r = requests.post(POST_URL, headers=headers, data=payload)
	
	if r.status_code == 200:
		ident = r.json()['id']
		if not r.json()['searching']:
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


def norbert2_get(person_id):
	
	# get Voilanorbert API key
	parser = SafeConfigParser()
	parser.read('config.txt')
	API_TOKEN = parser.get('norbert_v2', 'api_token')
	
	GET_URL = "https://api.voilanorbert.com/2016-01-04/contacts/"
	headers = {'api-token': API_TOKEN}
	payload = {'id': person_id }
	email = None
	abort = False # hack because the GET sometimes can't find the post'ed ID which raises a StopIteration exception.
	
	r = requests.get(GET_URL, headers=headers, params=payload)
	records = r.json()['result']
	
	# is Norbert still searching for the email addr?
	try:
		record = (rec for rec in records if rec['id']==person_id).next()
	except:
		# give up on this one
		abort = True
		return False, email, abort
	if not record['searching']:
		# search finished
		if record['email']:
			# email found
			email = record['email']['email']
		else:
			# email not found
			pass
	
	return record['searching'], email, abort


def norbert2(name, domain):
	
	email = None
	
	# initial query
	id_no, email, status_code = norbert2_post(name, domain)
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
				searching, email, abort = norbert2_get(id_no)
				if abort:
					break
				count += 2
	
	return email, status_code

	