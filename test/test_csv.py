import csv
import sys

with open(sys.argv[1], 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print row
