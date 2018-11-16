import os
import sys
import random
import time

nTrials = int(sys.argv[1])
seed = int (sys.argv[2])
random.seed(seed)
start = 0
print "\n\n\nCreating submission scripts for:"
print "\t", nTrials, " fault injection trials in 8 scripts"
print "\t", seed, " RNG seed"
print "\n\n\n"

if len(sys.argv) >=4:
    start = int(sys.argv[3])
for i in range(0, start):
    t = random.randint(0,50000000)
    print "Skippig trial %d with seed %d" %(i, t)


# TODO: set this variable to where "test_HPCCG" exists
exe_path = "TODO: SET ME"
flipit_dir = os.environ["FLIPIT_PATH"]
i = start
while i < nTrials:

    #write the pbs submission file
    outfile = open("fault" + str(i) + ".pbs", "w")
    outfile.write("#!/bin/bash\n"
                "#PBS -l select=1:ncpus=8:mem=2gb\n"
                "#PBS -l walltime=09:00:00\n"
                #"#PBS -j oe\n"
        "#PBS -A jr5\n"
                "#PBS -N ECE_6930_HW3\n"
                "module load gcc/4.8.1\n"
                "module load mpich\n"
                "module list\n")
    j = 0
    while j < (nTrials-start)/8 + 1:
    	if i+j < nTrials:
            outfile.write("\nmkdir $PBS_O_WORKDIR/test_" + str(i+j)\
                	+ "\ncd $PBS_O_WORKDIR/test_" +str(i+j)\
                	+ "\nmpirun -n 8 " + exe_path + "/test_HPCCG 32 32 32 --stateFile " + flipit_dir + "/.HPCCG --numberFaulty 1 --faulty "\
                	#+ "\nmpirun -n 8  /home/jonccal/teaching/HPCCG-1.0/test_HPCCG 32 32 32 --stateFile /home/jonccal/research/FlipIt//.HPCCG --numberFaulty 1 --faulty "\
                    + str(random.randint(0, 7)) + " " \
                	+ str(random.randint(0,50000000)) + " &> test_" +str(i+j) + ".txt\n")

	
        j += 1
    
    #submit the file
    outfile.close()
    if i <= nTrials:
        print "Launching job..."#, i
        os.system("qsub fault" + str(i) + ".pbs")

    i += j
    

