# ECE 4930

my_grades = {"project":[73.0],
					   "hw":[72.81],
					   "paper":[69.07],
					   "pres":[76.19],
					   "participation":[100.0],
					   "lecture":[92.0],
					   "final":[79.43]}

#class_grades = {"hw_and_quizzes":[36.5,56.0,44.0,42.0],
#						  "tests":[46.0,45.6],
#						  "final":[50.0]}
	  

def average(numbers):
	total = float(sum(numbers))
	total = total / len(numbers)
	return total
	
def get_average(x):
	project = average(my_grades["project"])
	hw = average(my_grades["hw"])
	paper = average(my_grades["paper"])
	pres = average(my_grades["pres"])
	part = average(my_grades["participation"])
	lecture = average(my_grades["lecture"])
	final = average(my_grades["final"])
	return project*.20+hw*.15+paper*.05+pres*.05+part*.10+lecture*.25+final*.20

	
def get_letter_grade(score):
	if score >= 90:
		return "A"
	elif score >= 80:
		return "B"
	elif score >= 70:
		return "C"
	elif score >= 60:
		return "D"
	else:
		return "F"

print "ECE 4930 - HPC Fault Tolerance"
print "Current grade: %s (%s)" % (get_letter_grade(get_average(my_grades)), get_average(my_grades))
#print "Class average: %s (%s)" % (get_letter_grade(get_average(class_grades)), get_average(class_grades))
