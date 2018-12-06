import os

print("Running 'total_bitflips.py'...\n")

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
		
print("Calculating single & double bit-flip errors...\n")
for date in dates:
	for phase in list(phases_dict.keys()):
		if phase in os.listdir(path_to_reports + date):
			nodes = os.listdir(path_to_reports + date + '/' + phase)
			
			for node in nodes:
				f = open(path_to_reports + date + '/' + phase + '/' + node, 'r')
				
				lines = []
				for line in f:
					lines.append(line)

				for i in range(len(lines)):
					if lines[i][8:17] == 'Aggregate':
						phases_dict[phase][0] += int(lines[i+9][38:])
						phases_dict[phase][1] += int(lines[i+18][38:])

print("\n====RESULTS====\n")
for key in phases_dict:
	print("{0}:\n\tTotal Single Bit-flip Errors = {1}\n\tTotal Double Bit-flip Errors = {2}\n\n".format(key,phases_dict[key][0],phases_dict[key][1]))

