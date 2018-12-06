import os

print("Running 'bitflips_by_day.py'...\n")

# specify path to log files
path_to_reports = '../ecc-gpu-reports/'

# all dates in a list
dates = os.listdir(path_to_reports)

phases_dict = {}
print("Collecting dates and phases...\n")
for date in dates:
	phases = os.listdir(path_to_reports + date)
	
	for phase in phases:
		if phase not in list(phases_dict.keys()):
			phases_dict[phase] = [0,0]


phases_dates = {}
for x in phases_list:
	phases_dates[x] = []


for phase in list(phases_dates.keys()):
	for date in dates:
		if phase in os.listdir(path_to_reports + date):
			phases_dates[phase].append([date,0,0])
			

for key in phases_dates:
	for elem in phases_dates[key]:
		for node in os.listdir(path_to_reports + elem[0] + '/' + key):
			f = open(path_to_reports + elem[0] + '/' + key + '/' + node, 'r')
			
			lines = []
			for line in f:
				lines.append(line)
				
			for i in range(len(lines)):
				if lines[i][8:17] == 'Aggregate':
					elem[1] += int(lines[i+9][38:])
					elem[2] += int(lines[i+18][38:])


for key in phases_dates:
	print(key+'')
	for elem in phases_dates[key]:
		if len(elem) == 1:
			print('\t{}'.format(elem[0]))
		else:
			print('\t{}\n\t{}\n\t{}'.format(elem[0],elem[1],elem[2]))
	print('\n')