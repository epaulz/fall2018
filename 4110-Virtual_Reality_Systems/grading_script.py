# CPSC 4110

my_grades = {'attendance':[76.0],
				       'quiz_assignments':[68.75],
					   'proposal_pres':[90.0],
					   'critique':[66.67],
					   'midterm':[86.36],
					   'prelim_demo':[100.0],
					   'final_demo':[95.05],
					   'final':[20.0]}

#class_grades = {"hw_and_quizzes":[36.5,56.0,44.0,42.0],
#						  "tests":[46.0,45.6],
#						  "final":[50.0]}
	  

def average(numbers):
	total = float(sum(numbers))
	total = total / len(numbers)
	return total
	
def get_average(x):
	attendance = average(my_grades['attendance'])
	quiz_assignments = average(my_grades['quiz_assignments'])
	proposal_pres = average(my_grades['proposal_pres'])
	critique = average(my_grades['critique'])
	midterm = average(my_grades['midterm'])
	prelim_demo = average(my_grades['prelim_demo'])
	final_demo = average(my_grades['final_demo'])
	final = average(my_grades['final'])
	
	return attendance*.02 + quiz_assignments*.10 + proposal_pres*.08 + critique*.03 + midterm*.20 + prelim_demo*.16 + final_demo*.16 + final*.25

	
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

print "CPSC 4110 - Virtual Reality"
print "Current grade: %s (%s)" % (get_letter_grade(get_average(my_grades)), get_average(my_grades))
#print "Class average: %s (%s)" % (get_letter_grade(get_average(class_grades)), get_average(class_grades))
