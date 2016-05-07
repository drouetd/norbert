# -*- coding: utf-8 -*-

import csv

def dict_read_csv(filename):
	""" Assumes there is a header row. Returns a list of dics."""
	records = []
	with open(filename) as f:
		f_csv = csv.DictReader(f, skipinitialspace=True)
		for row in f_csv:
			print row
			records.append(row)
	
	return records


def write_to_csv(filename, fields, records):
	""" Writes a list of dictionaries to a csv file. """
	with open(filename, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
		writer.writeheader()
		writer.writerows(records)
	return


def strip_extra_fields(final_headers, records):
	
	stripped_records = []
	# identify the keys to remove
	ban = [k for k in records[0].keys() if k not in final_headers]
	for rec in records:
		for k in ban:
			if k in rec:
				del rec[k]
		stripped_records.append(rec)
	
	return stripped_records


def generate_output_filename(file_name, suffix):
	""" Adds a suffix to the input csv to track progress through data pipeline. """
	parts = file_name.split('.')
	if len(parts) == 2:
		output_filename = parts[0] + suffix + '.' + parts[1]
	return output_filename



if __name__ == "__main__":
	
	# read a csv file with headers
	fname = "Data/mesi_ctrl.csv"
	data = dict_read_csv(fname)
	
	# modify the data
	for d in data:
		d['salutation'] = "Mr."
	
	# write to file
	headers = ['contact', 'salutation', 'company', 'title', 'department', 'phone', 'mobile', 'city', 'province', 'country', 'website', 'email']
	strip_extra_fields(headers, data)
	write_to_csv("Data/mesi_webtest.csv", headers, data)
	