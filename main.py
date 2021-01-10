import boto
import boto.s3
import sys
from boto.s3.key import Key
import requests
from datetime import timedelta, datetime

def percent_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()

def upload(filename,enter_date):

  AWS_ACCESS_KEY_ID = 'AKIAJHQ7I5KGYVIOUNQQ'
  AWS_SECRET_ACCESS_KEY = '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'
  bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
  conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

  bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)
  print('Uploading {} to Amazon S3 bucket {}'.format(filename, bucket_name))
  k = Key(bucket)
  k.key = str(enter_date)
  k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

def create_file(episodes, enter_date):
	file_name = str(enter_date)+'.txt'
	with open(file_name, 'w') as log:
		for key, value in episodes.items():
			log.write('{} aired {} in {}\n'.format(key, value, enter_date))
	upload(file_name, enter_date)


active = True
while active:
	print('TAMAZE API')
	print('')
	print("0) Exit")
	print('1) Get Episode Details ')

	try:
		answer = input("Option: ")
		print('')

		if int(answer) == 1:
			input_date = input("Enter Date: ")
			print('You selected {} this date'.format(input_date))
			get_month = []
			get_month.append(input_date)
			dates = []
			finalized_list = []

			for month_ in get_month:

				month, year = int(month_.split('-')[1]), int(month_.split('-')[0])
				print(month, year)
				day = timedelta(days=1)
				date1 = datetime(year, month, 1)
				d = date1

				while d.month == month:
					dates.append(d.strftime('%Y-%m-%d'))
					print(d.strftime('%Y-%m-%d'))
					d += day
					response = requests.get(
						'http://api.tvmaze.com/schedule/web?date={}'.format(d.strftime('%Y-%m-%d')))
					get_data = response.json()
					for data in get_data:
						finalized_list.append(data['name'])
			freq = {}
			for item in finalized_list:
				if item in freq:
					freq[item] += 1
				else:
					freq[item] = 1

			create_file(freq, input_date)
			print('')

		elif int(answer) == 0:
			active = False
			print('Bye')
			print('')
		else:
			print('')
			print("0) Exit")
			print('')
	except Exception as e:
		print('')
		print(e)
		print("NameError: Please Use Numbers Only")
		print('')
