from formatting import dict_read_csv
from formatting import write_to_csv
from formatting import strip_extra_fields
from formatting import generate_output_filename
from norbert2 import find_email
	
if __name__ == "__main__":

	# read a csv file with headers
	fname = "Data/corps_web.csv"
	data = dict_read_csv(fname)

	# add the emails
	for d in data:
		d['email'] = find_email(d['contact'], d['website'])
		print d['contact'], ": ", d['email']

	# write to file
	output_file = generate_output_filename(fname, '_email')
	headers = ['contact', 'salutation', 'company', 'title', 'department', 'phone', 'mobile', 'city', 'province', 'country', 'website', 'email']
	strip_extra_fields(headers, data)
	#headers = ['contact', 'company', 'website', 'email']
	write_to_csv(output_file, headers, data)
	print "\nDone!\n"
	
