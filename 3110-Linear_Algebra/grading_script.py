# MATH 3110

my_grades = {'hw':[100.0,86.67,87.5,80.0,87.5,95.0,45.0],
					   'quiz':[70.0,100.0,80.0],
					   'tests':[95.0,72.5],
					   'final':[5.0]}
'''
class_grades = {"hw_and_quizzes":[36.5,56.0,44.0,42.0],
						  "tests":[46.0,45.6],
						  "final":[50.0]}
'''	  

def average(numbers):
	total = float(sum(numbers))
	total = total / len(numbers)
	return total
	
def get_average(x):
	hw = average(my_grades['hw'])
	quiz = average(my_grades['quiz'])
	tests = average(my_grades['tests'])
	final = average(my_grades['final'])
	return hw*.20 + quiz*.10 + tests*.40 + final*.30

	
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

print "MATH 3110 - Linear Algebra"
print "Current grade: %s (%s)" % (get_letter_grade(get_average(my_grades)), get_average(my_grades))
#print "Class average: %s (%s)" % (get_letter_grade(get_average(class_grades)), get_average(class_grades))
