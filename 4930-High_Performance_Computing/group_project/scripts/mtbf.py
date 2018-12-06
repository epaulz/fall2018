import os
import pandas as pd

# specify path to log files
path_to_reports = '../ecc-gpu-reports/'

# all dates in a list
dates = os.listdir(path_to_reports)

phases_dict = {}
previous = 0
tot_failures = 0

for date in dates:
	for phase in os.listdir(path_to_reports + date):
		for node in os.listdir(path_to_reports + date + '/' + phase):
			f = open(path_to_reports + date + '/' + phase + '/' + node)
			
			lines = []
			for line in f:
				lines.append(line)
				
			for i in range(len(lines)):
				if lines[i][8:16] == 'Volatile':
					if previous > 0 and int(lines[i+9][38:]) == 0:
						tot_failures += 1
						previous = 0
						break
					else:
						previous = int(lines[i+9][38:])
						break
				
		if phase not in list(phases_dict.keys()):
			phases_dict[phase] = tot_failures
		else:
			phases_dict[phase] += tot_failures
		
		previous = 0
		tot_failures = 0
		
for key in phases_dict:
	print('{}: {}'.format(key,phases_dict[key]))
