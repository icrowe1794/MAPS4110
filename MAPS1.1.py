import pandas as pd
from IPython.display import display

class Student:
    def __init__(self, name, major):  # Could end up wanting email, password, etc..? Who knows
        self.name = name  # If this even matters?
        self.major = major  # Maybe relevant
        self.email = ''  # Unnecessary?
        self.gender = ''  # Unnecessary?
        # completedCourses will be a list of course objects
        self.completedCourses = []  # This will also be used to check Freshmen / Sophomore / Junior / Senior?
        # upcomingSemester should be removed from here and exist as a regular variable?
        self.upcomingSemester = 'Fall'


class Course:
    def __init__(self, name, credits):
        self.name = name  # Class name ex: CMPS 411
        self.title = ''  # Full name ex: 'INTRODUCTION TO DATA SCIENCE'
        self.credits = credits  # Number of class credits/hours
        self.preReq = ''  # Requirement must have passed already
        self.curReq = ''  # Requirement but can be currently taking
        self.rank = 0
        self.availSemester = ''  # S/F/Summer?
        self.avgNumAvail = 0  # Idk if these differ based on Sp/Fa/Sum
        self.avgSize = 0  # I guess this is also important for weighting a class (Combine with avgNumAvail)
        self.timeSlots = []  # Prob not messing with this?
        self.majorReq = []  # (Not needed?) For specific classes that are needed for specific majors?
        self.teacher = []  # List of teachers for this class in upcoming semester (If we even have this info)
        Courses.append(self)
        # print("Class '" + self.name + "' created!")

    def addPreReq(self, name):  # Adjust?
        self.preReq.append(name)

    def removePreReq(self, name):  # Is remove correct here?
        self.preReq.remove(name)

    def addCurReq(self, name):  # Adjust?
        self.curReq.append(name)

    def removeCurReq(self, name):  # Is remove correct here?
        self.curReq.remove(name)

    def setAvailSemester(self, sem):
        self.availSemester = sem

    def setAvgNumAvail(self, num):
        self.avgNumAvail = num

    def setAvgSize(self, num):
        self.avgSize = num

    def changeName(self, name):
        self.name = name

    def changeTitle(self, title):
        self.title = title

    def changeCredits(self, credits):
        self.credits = credits

# Maybe 'AND' won't be assumed?
# If type string (not another list), then it'll be 'NONE', a single class, or 'SENIOR'
# Else check length then start searching through to identify more complex requirements

# I think I want to have prereqs setup within a list themselves, 'AND' is generally assumed, unlike 'OR' or 'CURR' isn't
# Requiring 2 classes as prereqs would look like ('CMPS 3900', 'MATH 2230')
# Requiring 1 of 2 classes would look like (('OR', 'CMPS 3900', 'MATH 2230'))
# Requiring 1 class, as well as 1 of 2 classes would look like ('CMPS 3400', ('OR', 'CMPS 3900', 'MATH 2230'))
# A class that is a requirement but can be taken currently would look like (('CURR', 'BIOL 1510'))
# A class that requires senior status (current semester puts you past 90+ credit hours) is labled as 'SENIOR'
# ex: ('CMPS 3900', 'SENIOR') would mean it requires 3900 AND senior status
# Will need to rework how I check through prereqs though to implement all this

# General class list below: (Based on my college scheduling)
#                English: Some options here?
generalCMPS = [('ENGL 1010', 'None', 'Fall/Spring/Summer', 'FRESHMAN COMPOSITION', 3),
               ('ENGL 1020', 'ENGL 1010', 'Fall/Spring/Summer', 'CRITICAL READING AND WRITING', 3),
               ('ENGL 2320', 'ENGL 1020', 'Fall/Spring/Summer', 'AMERICAN LITERATURE', 3),
               ('ENGL 3220', 'ENGL 1020', 'Fall/Spring/Summer', 'INTRODUCTION TO PROFESSIONAL AND TECHNICAL WRITING', 3),
               # Computer Science:
               # CMPS 1610: Could include eligible to enroll in math 1610 as prereq?
               # CMPS 2800: Recheck prereqs?
               ('CMPS 1610', 'None', 'Fall/Spring/Summer', 'ALGORITHM DESIGN AND IMPLEMENTATION I', 3),
               ('CMPS 2800', 'CMPS 1610', 'Fall/Spring/Summer', 'ALGORITHM DESIGN AND IMPLEMENTATION II', 3),
               ('CMPS 2850', 'CMPS 2800', 'Fall/Spring/Summer', 'SOFTWARE ENGINEERING', 3),
               ('CMPS 3400', 'CMPS 2800', 'Fall/Spring/Summer', 'INTRODUCTION TO DATA SCIENCE', 3),
               ('CMPS 3750', 'CMPS 2800', 'Spring', 'COMPUTER ARCHITECTURE', 3),
               ('CMPS 3900', 'CMPS 2800', 'Fall/Spring/Summer', 'DATA STRUCTURES', 3),
               ('CMPS 4010', 'CMPS 3900', 'Fall', 'SURVEY OF PROGRAMMING LANGUAGES', 3),
               ('CMPS 4110', 'CMPS 3900 and Senior', 'Fall', 'CAPSTONE I', 3),
               ('CMPS 4310', 'CMPS 3900 and CMPS 3750 (Current/Past)', 'Fall/Spring/Summer', 'OPERATING SYSTEMS', 3),
               ('CMPS 4340', 'CMPS 3900 and MATH 2230', 'Fall', 'FUNDAMENTAL ALGORITHMS', 3),
               ('CMPS 4390', 'CMPS 3400 or CMPS 3900', 'Spring', 'DATABASE SYSTEMS', 3),
               ('CMPS 4410', 'CMPS 3400', 'Fall', 'ARTIFICIAL INTELLIGENCE', 3),
               ('CMPS 4510', 'CMPS 3400', 'Fall', 'DATA MINING', 3),
               # 455: One of the required electives?
               ('CMPS 4550', 'CMPS 2800 and MATH 2000', 'Fall', 'COMPUTATIONAL ASPECTS OF GAME PROGRAMMING', 3),
               ('CMPS 4700', 'CMPS 3400 or MATH 3800', 'Spring', 'MACHINE LEARNING', 3),
               ('CMPS 4730', 'CMPS 3400 and MATH 2000', 'Spring', 'INTRODUCTION TO COMPUTER VISION', 3),
               ('CMPS 4820', 'CMPS 4110 (Current/Past) and Senior', 'Fall/Spring/Summer',
                'CURRENT TRENDS IN COMPUTER SCIENCE', 3),
               # Math: Options?
               # Math 1750: Include this?, requires 1610
               # Math 2000: Include MATH 1750 req?
               ('MATH 1610', 'None', 'Fall/Spring/Summer', 'COLLEGE ALGEBRA', 3),  # Ignored prereq
               ('MATH 1620', 'MATH 1610', 'Fall/Spring/Summer', 'TRIGONOMETRY', 3),
               ('MATH 1750', 'MATH 1610', 'Fall/Spring/Summer', 'PRE-CALCULUS WITH TRIGONOMETRY', 5),  # Double check this is needed?
               ('MATH 2000', 'MATH 1750', 'Fall/Spring/Summer', 'CALCULUS I', 5),  # Ignored prereq
               ('MATH 2010', 'MATH 2000', 'Fall/Spring', 'CALCULUS II', 5),
               ('MATH 2230', 'MATH 2000', 'Fall/Spring', 'FOUNDATIONS OF DISCRETE MATHEMATICS', 3),
               ('MATH 3600', 'MATH 2010 and MATH 2230', 'Fall/Spring', 'LINEAR ALGEBRA I', 3),
               ('MATH 3800', 'MATH 2010', 'Fall/Spring', 'MATHEMATICAL STATISTICS I', 3),
               ('MATH 3920', 'MATH 2010 and CMPS 2800', 'Fall/Spring', 'NUMERICAL METHODS', 3),
               # Biology:
               ('BIOL 1510', 'None', 'Fall/Spring/Summer', 'GENERAL BIOLOGY I', 3),  # Ignored prereq
               ('BIOL 1520', 'BIOL 1510 (Current/Past)', 'Fall/Spring/Summer', 'GENERAL BIOLOGY LAB I', 1),
               ('BIOL 1530', 'BIOL 1510', 'Fall/Spring/Summer', 'GENERAL BIOLOGY II', 3),
               ('BIOL 1540', 'BIOL 1530 (Current/Past)', 'Fall/Spring/Summer', 'GENERAL BIOLOGY LAB II', 1),
               # Physics:
               ('PHYS 2210', 'MATH 2000 (Current/Past)', 'Fall/Spring', 'GENERAL PHYSICS', 3),
               ('PLAB 2230', 'PHYS 2210 (Current/Past)', 'Fall/Spring', 'GENERAL PHYSICS LABORATORY', 1),
               # The rest:
               ('ART 1050', 'None', 'Fall/Spring/Summer', 'SURVEY OF WORLD ART HISTORY I', 3),  # Options?
               ('HIST 1010', 'None', 'Fall/Spring/Summer', 'WESTERN CIVILIZATION TO 1500', 3),  # Options?
               ('COMM 2110', 'None', 'Fall/Spring/Summer', 'INTRODUCTION TO PUBLIC SPEAKING', 3),  # Options?
               ('ECON 2010', 'None', 'Fall/Spring/Summer', 'PRINCIPLES OF ECONOMICS (MACROECONOMICS)', 3),  # Options?
               ('SOC 1010', 'None', 'Fall/Spring/Summer', 'INTRODUCTORY SOCIOLOGY', 3),  # Options?
               ('ELEC 1010', 'None', 'Fall/Spring/Summer', 'UNKNOWN ELECTIVE?', 3)]  # Options

Courses = []  # Full list of course objects?

# Seems like some of the course information is inconsistent between workday/school catalog (Keep this in mind I guess?)
# For example, pretty sure there were cases where prereqs were different, and or semester availability differed?


def addCoursesList(courseList):  # Converts basic list into course objects?
    for course in courseList:
        tempCourse = Course(course[0], course[4])
        tempCourse.changeTitle(course[3])
        tempCourse.setAvailSemester(course[2])
        if course[1] != 0:
            tempCourse.preReq = course[1]
        tempCourse.availSemester = course[2]


# Will want to input a Student here? (completedClasses will vary between students)
# Each student will ideally have a different 'Major' as well (courseList will vary based on Major)
# upcomingSemester should be the same for everyone?
def listOfEligibleCourses(courseList, upcomingSemester, completedClasses):  # Needs adjusting with new prereq setup
    eligible = []
    eligible2 = []
    ineligible = []
    for course in courseList:
        if course.name not in completedClasses:
            if upcomingSemester in course.availSemester:
                # ['None', 'ENGL 1010', 'CMPS 1610', 'MATH 1610', 'MATH 1620', 'MATH 2000', 'BIOL 1510', 'BIOL 1520', 'HIST 1010']
                for completed in completedClasses:
                    if completed in course.preReq:
                        eligible2.append(course.name)
                        eligible.append((course.name, course.rank, course.availSemester))
                        break
    for course in courseList:
        if (course.name not in eligible2) and (course.name not in completedClasses):
            ineligible.append((course.name, course.preReq, course.availSemester))
                    # else:
                    #     ineligible.append((course.name, course.preReq, course.availSemester))
            # else:
            #     for completed in completedClasses:
            #         if completed in course.preReq:
            #             ineligible.append((course.name, 'Eligible', course.availSemester))
            #             break
                    # else:
                    #     ineligible.append((course.name, course.preReq, course.availSemester))
    return eligible, ineligible


def classRanker(courseList):
    for course in courseList:
        ranking=0
        for course2 in courseList:
            if course.name in course2.preReq:
                ranking=ranking+1
        course.rank=ranking
    for course in courseList:
        for course2 in courseList:
            if course.name in course2.preReq:
                course.rank=course.rank+course2.rank


def selectSomeClasses(courseList, upcomingSemester, completedClasses, eligibleList):
    for course in eligibleList:
        pass
    pass


addCoursesList(generalCMPS)  # Creating the course objects, each object automatically adds itself to Courses[]
classRanker(Courses)


# Might want this as it's own def/method?
# More in-depth display of classes?
for course in Courses:
    print('Name: ' + course.name)
    print('Title: ' + course.title)
    print('PreReq: ' + course.preReq)
    print('Available: ' + course.availSemester)
    print()


# Might want this as it's own def/method?
# Simple display of classes in full Courses list, total number, and combined credits
temp = []
creditCount = 0
for course in Courses:
    temp.append(course.name)  # Grabbing just the course name for a simple list
    creditCount += course.credits  # Summing up the total credits, could be useful to make sure target for grad is hit
print(temp)
print('Length: ' + str(len(temp)))
print('Total Credits: ' + str(creditCount))
print()

completedCourses = ['None']
demoList1 = ['None', 'ENGL 1010', 'CMPS 1610', 'MATH 1610', 'MATH 1620', 'MATH 1750', 'BIOL 1510', 'BIOL 1520', 'HIST 1010']
demoList2 = ['None', 'ENGL 1010', 'CMPS 1610', 'MATH 1610', 'MATH 1620', 'MATH 1750', 'MATH 2000', 'BIOL 1510', 'BIOL 1520', 'HIST 1010', 'CMPS 2800', 'ENGL 1020', 'ART 1050', 'SOC 1010']
el, inel = listOfEligibleCourses(Courses, 'Summer', demoList2)



# Extra spacing above, can be removed later
eligible=pd.DataFrame(el,columns=['Class', 'Importance', 'Semester Offered'])
ineligible=pd.DataFrame(inel,columns=['Class', 'Prerequisites', 'Semester Offered'])
pd.set_option('display.max_columns', None)
print('-------ELIGIBLE & AVAILABLE-------')
display(eligible.sort_values('Importance', ascending=False))
print('\n\n')
print('-------NOT ELIGIBLE/AVAILABLE-------')
display(ineligible.sort_values('Class', ascending=True))
# Will end up wanting to implement user input for decisions...
# How many credit hours do you want to take?
# Do you want to take summer courses?
# If so, how many credit hours during the summer?
# How many semesters do you want to generate schedules for?
