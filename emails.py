# -*- coding: utf-8 -*-

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
	
	return file_name


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
	fname = parse_args()
	data = dict_read_csv(fname)

	# add the emails
	for d in data:
		d['email'], status = find_email(d['contact'], d['website'], norbert1)
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
	
	save_to_file(fname, data)
	print "\nDone!\n"
	
