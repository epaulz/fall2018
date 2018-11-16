# CPSC 4110

my_grades = {"exams":[],
						"final":[],
						"sessions":[],
						"lab_exam":[]}

class_grades = {"hw_and_quizzes":[36.5,56.0,44.0,42.0],
						  "tests":[46.0,45.6],
						  "final":[50.0]}
	  

def average(numbers):
	total = float(sum(numbers))
	total = total / len(numbers)
	return total
	
def get_average(x):
	exams = average(my_grades["exams"])
	final = average(my_grades["final"])
	sessions = average(my_grades["sessions"])
	lab_exam = average(my_grades["lab_exam"])
	return exams*.60 + final*.25 + sessions*.10 + lab_exam*.05

	
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
print "Class average: %s (%s)" % (get_letter_grade(get_average(class_grades)), get_average(class_grades))
