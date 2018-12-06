# MATH 3110

my_grades = {'hw':[(10.0/10)*100,(13.0/15)*100,(17.5/20)*100,(16.0/20)*100,(17.5/20)*100,(17.0/30)*100,(19.0/20)*100,(9.0/20)*100],
				        'quiz':[(3.5/5)*100,(5.0/5)*100,(4.0/5)*100,(0.0/5)*100],
						'midterms':[(19.0/20)*100,(14.5/20)*100],
						'final':[80.0] }
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
	midterms = average(my_grades['midterms'])
	final = average(my_grades['final'])
	return hw*.20 + quiz*.10 + midterms*.40 + final*.30

	
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
