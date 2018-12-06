import os
import pandas as pd

# specify path to log files
path_to_reports = '../ecc-gpu-reports/'

# all dates in a list
dates = os.listdir(path_to_reports)

nodes_list = []
flips_list = []

for date in dates:
	for phase in os.listdir(path_to_reports + date):
		#print("\t" + phase)
		for node in os.listdir(path_to_reports + date + '/' + phase):
			if node not in nodes_list:
				nodes_list.append(node)
				flips_list.append(0)
				
			f = open(path_to_reports + date + '/' + phase + '/' + node)
			
			lines = []
			for line in f:
				lines.append(line)
				
			for i in range(len(lines)):
				if lines[i][8:17] == 'Aggregate':
					flips_list[nodes_list.index(node)] += (int(lines[i+9][38:]) + int(lines[i+18][38:]))
					
#for node in nodes_list:
#	print("{},{}".format(node,flips_list[nodes_list.index(node)]))
	
d = {}
for node in nodes_list:
	d[str(node)] = int(flips_list[nodes_list.index(node)])
	
df = pd.DataFrame.from_dict(data=d, orient='index')
df.to_csv('./output.csv')