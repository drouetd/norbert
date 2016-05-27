# -*- coding: utf-8 -*-

import time
from utils import dict_read_csv
from utils import write_to_csv
from utils import strip_extra_fields
from utils import generate_output_filename
from norbert import norbert1
from norbert import norbert2	

def parse_args():
	file_name = raw_input("Path to CSV file to process: ")
	if not file_name:
		# use test file
		file_name = "Data/corps_web.csv"
	
	version = raw_input("Version of the Norbert API to use: v1 or v2 (default)? ")
	if not version:
		# use default version
		version = "v2" 
	return file_name, version


def save_to_file(filename, records):
	""" Save data before quitting."""
	output_file = generate_output_filename(filename, '_email')
	headers = ['contact', 'salutation', 'company', 'title', 'department', 'phone', 'mobile', 'city', 'province', 'country', 'website', 'email']
	strip_extra_fields(headers, records)
	write_to_csv(output_file, headers, records)
	return


def find_email(name, domain, api_wrapper):
	email, status = api_wrapper(name, domain)
	return email, status


if __name__ == "__main__":

	# read a csv file with headers
	fname, api_version = parse_args()
	data = dict_read_csv(fname)
	
	# select wrapper according to version of api to use
	if api_version == "v1":
		api_wrapper = norbert1
	else:
		api_wrapper = norbert2
	
	# search for emails
	for d in data:
		# only query if contact has website and no email already listed
		if d.get('website') and not d.get('email'):
			d['email'], status = find_email(d['contact'], d['website'], api_wrapper)
			if status == 200:
				print d['contact'], ": ", d['email']
		
			elif status == 400:
				print "Status code: %d. Skipping %s" % (status, d['contact'])
			
			elif status == 401:
				print "Status code: %d for %s. Quitting..." % (status, d['contact'])
				save_to_file(fname, data)
				sys.exit()
			
			elif status == 402:
				print "Status code: %d for %s. Quitting..." % (status, d['contact'])
				save_to_file(fname, data)
				sys.exit()
			
			elif status == 410:
				print "Status code: %d ( BUY MORE CREDITS!) for %s. Quitting..." % (status, d['contact'])
				save_to_file(fname, data)
				sys.exit()
			
			elif status == 429:
				print "%s: too many requests. Skipping and sleeping 5 secs" % d['contact']
			
			elif status == 502:
				print "%s: email not found." % d['contact']
				
			else:
				print "%s: UNDEFINED - Status code: %d. Skipping." % (d['contact'], status)
				
			# TODO: add more sophisticated rate-limiting
			time.sleep(1.2)
		else:
			# already have email or no website is listed
			reason = "no reason"
			if not d.get('website'):
				reason = "no website"
			elif d.get('email'):
				reason = "already has email"
			print d['contact'], ": skipping -> %s" % reason
	
	save_to_file(fname, data)
	print "Done!\n"
	
