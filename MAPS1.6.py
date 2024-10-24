# ttkbootstrap must be installed 
# use 'pip install pillow requests' if pillow and requests dont work
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.widgets import Meter
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import END
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
import time
import pandas as pd
from IPython.display import display
Image.CUBIC = Image.BICUBIC


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
        # self.preReq.append(name)
        pass

    def removePreReq(self, name):  # Is remove correct here?
        # self.preReq.remove(name)
        pass

    def addCurReq(self, name):  # Adjust?
        # self.curReq.append(name)
        pass

    def removeCurReq(self, name):  # Is remove correct here?
        # self.curReq.remove(name)
        pass

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


# General class list below: (Based on my college scheduling)
#                English: Some options here?
generalCMPS = [('ENGL 1010', 'None', 'Fall/Spring/Summer', 'FRESHMAN COMPOSITION', 3),
               ('ENGL 1020', 'ENGL 1010', 'Fall/Spring/Summer', 'CRITICAL READING AND WRITING', 3),
               ('ENGL 2320', 'ENGL 1020', 'Fall/Spring/Summer', 'AMERICAN LITERATURE', 3),
               ('ENGL 3220', 'ENGL 1020', 'Fall/Spring/Summer', 'INTRODUCTION TO PROFESSIONAL AND TECHNICAL WRITING', 3),
               # Computer Science:
               # CMPS 1610: Could include eligible to enroll in math 1610 as prereq?
               ('CMPS 1610', ('CURRENT', 'MATH 1610'), 'Fall/Spring/Summer', 'ALGORITHM DESIGN AND IMPLEMENTATION I', 3),
               ('CMPS 2800', 'CMPS 1610', 'Fall/Spring/Summer', 'ALGORITHM DESIGN AND IMPLEMENTATION II', 3),
               ('CMPS 2850', 'CMPS 2800', 'Fall/Spring/Summer', 'SOFTWARE ENGINEERING', 3),
               ('CMPS 3400', 'CMPS 2800', 'Fall/Spring/Summer', 'INTRODUCTION TO DATA SCIENCE', 3),
               ('CMPS 3750', 'CMPS 2800', 'Spring', 'COMPUTER ARCHITECTURE', 3),
               ('CMPS 3900', 'CMPS 2800', 'Fall/Spring/Summer', 'DATA STRUCTURES', 3),
               ('CMPS 4010', 'CMPS 3900', 'Fall', 'SURVEY OF PROGRAMMING LANGUAGES', 3),
               ('CMPS 4110', ('AND', 'CMPS 3900', 'SENIOR'), 'Fall', 'CAPSTONE I', 3),
               ('CMPS 4310', ('AND', 'CMPS 3900', ('CURRENT', 'CMPS 3750')), 'Fall/Spring/Summer', 'OPERATING SYSTEMS', 3),
               ('CMPS 4340', ('AND', 'CMPS 3900', 'MATH 2230'), 'Fall', 'FUNDAMENTAL ALGORITHMS', 3),
               ('CMPS 4390', ('OR', 'CMPS 3400', 'CMPS 3900'), 'Spring', 'DATABASE SYSTEMS', 3),
               ('CMPS 4410', 'CMPS 3400', 'Fall', 'ARTIFICIAL INTELLIGENCE', 3),
               ('CMPS 4510', 'CMPS 3400', 'Fall', 'DATA MINING', 3),
               # 455: One of the required electives?
               ('CMPS 4550', ('AND', 'CMPS 2800', 'MATH 2000'), 'Fall', 'COMPUTATIONAL ASPECTS OF GAME PROGRAMMING', 3),
               ('CMPS 4700', ('OR', 'CMPS 3400', 'MATH 3800'), 'Spring', 'MACHINE LEARNING', 3),
               ('CMPS 4730', ('AND', 'CMPS 3400', 'MATH 2000'), 'Spring', 'INTRODUCTION TO COMPUTER VISION', 3),
               ('CMPS 4820', ('AND', ('CURRENT', 'CMPS 4110'), 'SENIOR'), 'Fall/Spring/Summer',
                'CURRENT TRENDS IN COMPUTER SCIENCE', 3),
               # Math: Options?
               ('MATH 1610', 'None', 'Fall/Spring/Summer', 'COLLEGE ALGEBRA', 3),  # Ignored prereq
               ('MATH 1620', 'MATH 1610', 'Fall/Spring/Summer', 'TRIGONOMETRY', 3),
               ('MATH 2000', 'MATH 1620', 'Fall/Spring/Summer', 'CALCULUS I', 5),  # Ignored prereq
               ('MATH 2010', 'MATH 2000', 'Fall/Spring', 'CALCULUS II', 5),
               ('MATH 2230', 'MATH 2000', 'Fall/Spring', 'FOUNDATIONS OF DISCRETE MATHEMATICS', 3),
               ('MATH 3600', ('AND', 'MATH 2010', 'MATH 2230'), 'Fall/Spring', 'LINEAR ALGEBRA I', 3),
               ('MATH 3800', 'MATH 2010', 'Fall/Spring', 'MATHEMATICAL STATISTICS I', 3),
               ('MATH 3920', ('AND', 'MATH 2010', 'CMPS 2800'), 'Fall/Spring', 'NUMERICAL METHODS', 3),
               # Biology:
               ('BIOL 1510', 'None', 'Fall/Spring/Summer', 'GENERAL BIOLOGY I', 3),  # Ignored prereq
               ('BIOL 1520', ('CURRENT', 'BIOL 1510'), 'Fall/Spring/Summer', 'GENERAL BIOLOGY LAB I', 1),
               ('BIOL 1530', 'BIOL 1510', 'Fall/Spring/Summer', 'GENERAL BIOLOGY II', 3),
               ('BIOL 1540', ('CURRENT', 'BIOL 1530'), 'Fall/Spring/Summer', 'GENERAL BIOLOGY LAB II', 1),
               # Physics:
               ('PHYS 2210', ('CURRENT', 'MATH 2000'), 'Fall/Spring', 'GENERAL PHYSICS', 3),
               ('PLAB 2230', ('CURRENT', 'PHYS 2210'), 'Fall/Spring', 'GENERAL PHYSICS LABORATORY', 1),
               # The rest:
               ('ART 1050', 'None', 'Fall/Spring/Summer', 'SURVEY OF WORLD ART HISTORY I', 3),  # Options?
               ('HIST 1010', 'None', 'Fall/Spring/Summer', 'WESTERN CIVILIZATION TO 1500', 3),  # Options?
               ('COMM 2110', 'None', 'Fall/Spring/Summer', 'INTRODUCTION TO PUBLIC SPEAKING', 3),  # Options?
               ('ECON 2010', 'None', 'Fall/Spring/Summer', 'PRINCIPLES OF ECONOMICS (MACROECONOMICS)', 3),  # Options?
               ('SOC 1010', 'None', 'Fall/Spring/Summer', 'INTRODUCTORY SOCIOLOGY', 3),  # Options?
               ('ELEC 1010', 'None', 'Fall/Spring/Summer', 'UNKNOWN ELECTIVE', 3)]  # Options


Courses = []  # Full list of course objects?


def addCoursesList(courseList):  # Converts basic list into course objects?
    for course in courseList:
        tempCourse = Course(course[0], course[4])
        tempCourse.preReq = course[1]
        tempCourse.availSemester = course[2]
        tempCourse.title = course[3]


# Will want to input a Student here? (completedClasses will vary between students)
# Each student will ideally have a different 'Major' as well (courseList will vary based on Major)
# upcomingSemester should be the same for everyone?
def listOfEligibleCourses(courseList, upcomingSemester, completedClasses):  # Needs adjusting with new prereq setup
    eligible = []
    eligible2 = []  # This is being used because eligible[] ends up having multiple attributes per class, this just has the name
    ineligible = []
    unavailable = []
    for course in courseList:
        if course.name not in completedClasses:
            if upcomingSemester in course.availSemester:
                if checkPrereqs(course.preReq, completedClasses, courseList):
                    eligible2.append(course.name)  # Not used at the moment
                    eligible.append((course.name, course.rank, course.availSemester))
                else:
                    ineligible.append((course.name, writtenPrereq(course.preReq), course.availSemester))  # Adjust preReq output
            else:
                ineligible.append((course.name, writtenPrereq(course.preReq), course.availSemester))  # Adjust preReq output
                unavailable.append((course.name, course.preReq, course.availSemester))  # Adjust preReq output
    return eligible, ineligible


def writtenPrereq(preReq):
    output = 'Prerequisites: '
    if isinstance(preReq, str):
        if preReq == 'SENIOR':
            return 'You must be in the process of completing 90+ credit hours (senior status).'
        else:
            return f"Prerequisite: {preReq}"
    elif preReq[0] == 'AND':
        for i in range(len(preReq)-1):
            if isinstance(preReq[i+1], str):
                if i+2 > len(preReq)-1:
                    output += preReq[i+1] + '.'
                elif i+3 > len(preReq)-1:
                    output += preReq[i + 1] + ' and '
                else:
                    output += preReq[i+1] + ', '
        return output
    elif preReq[0] == 'OR':
        for i in range(len(preReq)-1):
            if isinstance(preReq[i+1], str):
                if i+2 > len(preReq)-1:
                    output += preReq[i+1] + '.'
                elif i+3 > len(preReq)-1:
                    output += preReq[i + 1] + ' or '
                else:
                    output += preReq[i+1] + ', '
        return output
    elif preReq[0] == 'CURRENT':  # Might need some adjusting down the line
        return 'Eligible to take ' + preReq[1] + '.'
    else:
        print('Error in writtenPrereq function?')
        print(isinstance(preReq, str))
        print(preReq)
        print()
        return preReq


def checkPrereqs(prereqs, completedCourses, allCourses):
    if isinstance(prereqs, str):  # Only one thing to check, should be: 'Class name', 'NONE', or 'SENIOR'?
        if prereqs in completedCourses or prereqs == 'None':
            return True
        else:
            return False  # Should this be in an 'else:'?
    elif prereqs[0] == 'AND':  # All conditions are met
        for i in range(len(prereqs)-1):
            if isinstance(prereqs[i+1], str):
                if prereqs[i+1] not in completedCourses:  # Only breaks if a condition isn't met
                    return False
            else:
                if not checkPrereqs(prereqs[i+1], completedCourses, allCourses):  # Only breaks if a condition isn't met
                    return False
        return True
    elif prereqs[0] == 'OR':  # At least one condition is met
        for i in range(len(prereqs)-1):
            if isinstance(prereqs[i+1], str):
                if prereqs[i+1] in completedCourses:  # Only breaks if a condition is met
                    return True
            else:
                if checkPrereqs(prereqs[i+1], completedCourses, allCourses):  # Only breaks if a condition is met
                    return True
        return False
    elif prereqs[0] == 'CURRENT':  # Will need to adjust this later to confirm the prereq is selected/suggested
        for course in allCourses:  # Grabbing the prereq's prereqs?
            if course.name == prereqs[1]:
                return checkPrereqs(course.preReq, completedCourses, allCourses)
        print('Error in checkEligible function, CURR course missing?')
        return False
    else:
        print('Error in checkEligible function?')
        print(isinstance(prereqs, str))
        print(prereqs)
        print()
        return False


def classRanker(courseList):  # This needs to be redone as well with new prereqs?
    for course in courseList:
        ranking = 0
        for char in course.name:
            if char.isdigit():
                multiplier = (6 - int(char))
                break
        for course2 in courseList:
            if course.name in course2.preReq:  # This part specifically needs adjusting
                ranking = ranking + 1
        course.rank = (1 + ranking) * multiplier
    for course in courseList:
        for course2 in courseList:
            if course.name in course2.preReq:  # This part specifically needs adjusting
                course.rank = course.rank + course2.rank


def selectSomeClasses(courseList, upcomingSemester, completedClasses, eligibleList):
    for course in eligibleList:
        pass
    pass





#GUI STUFF--

class MAPSScheduler(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")  # can change to any other theme

        self.title("MAPS")
        self.geometry("1600x1200")  # size of actual window

        self.selu_green = "#006747"
        self.selu_light_gold = "#FFD700"

        self.configure_styles() 
        self.create_widgets()  

        addCoursesList(generalCMPS)
        classRanker(Courses)

        self.popup_window = None # if we remove the popup, this can go

        self.results_visible = False #makes sure chart is NOT VISIBLE before pressing 'generate'

    def configure_styles(self): 
        style = self.style
        style.configure("TFrame", background=self.selu_green)
        style.configure("Custom.TLabel", foreground="white", background=self.selu_green, font=("Helvetica", 12))
        style.configure("Custom.TButton", background=self.selu_light_gold, foreground=self.selu_green, font=("Helvetica", 12, "bold"))
        style.configure("Semester.TButton", background=self.selu_light_gold, foreground=self.selu_green, font=("Helvetica", 12, "bold"))
        style.configure("Custom.TEntry", fieldbackground="white", foreground="black")
        style.configure("Custom.TCombobox", fieldbackground="white", foreground=self.selu_green)
        style.configure("Title.TLabel", foreground=self.selu_light_gold, background=self.selu_green, font=("Helvetica", 24, "bold"))

    def create_widgets(self):
        # main container frame
        main_container = ttk.Frame(self, style="TFrame")
        main_container.pack(fill=BOTH, expand=YES)

        # mcroll frame for main
        main_scrolled_frame = ScrolledFrame(main_container)
        main_scrolled_frame.pack(fill=BOTH, expand=YES)

        main_frame = ttk.Frame(main_scrolled_frame, style="TFrame", padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        title_label = ttk.Label(main_frame, text="MAPS", style="Title.TLabel")
        title_label.pack(pady=20)

        # hold input fields and meter
        content_frame = ttk.Frame(main_frame, style="TFrame")
        content_frame.pack(fill=X, pady=20)

        # frame for the input fields
        input_frame = ttk.Frame(content_frame, style="TFrame")
        input_frame.pack(side=LEFT, fill=Y)

        # Input fields
        ttk.Label(input_frame, text="Student Name:", style="Custom.TLabel").grid(row=0, column=0, sticky=W, pady=(10, 5))
        self.name_entry = ttk.Entry(input_frame, width=40, style="Custom.TEntry")
        self.name_entry.grid(row=0, column=1, sticky=W, pady=(10, 5))

        ttk.Label(input_frame, text="Major:", style="Custom.TLabel").grid(row=1, column=0, sticky=W, pady=(10, 5))
        self.major_entry = ttk.Entry(input_frame, width=40, style="Custom.TEntry")
        self.major_entry.grid(row=1, column=1, sticky=W, pady=(10, 5))

        ttk.Label(input_frame, text="Completed Classes:", style="Custom.TLabel").grid(row=2, column=0, sticky=W, pady=(10, 5))
        self.completed_entry = ttk.Entry(input_frame, width=40, style="Custom.TEntry")
        self.completed_entry.grid(row=2, column=1, sticky=W, pady=(10, 5))
        ttk.Label(input_frame, text="Enter classes separated by commas", foreground="lightgray", background=self.selu_green, font=("Helvetica", 8)).grid(row=3, column=1, sticky=W)

        # explands to show classes for input (probably getting removed later)
        expand_button = ttk.Button(input_frame, text="Expand", command=self.show_available_classes, style="Custom.TButton")
        expand_button.grid(row=2, column=2, padx=(5, 0), pady=(10, 5))  # row and column

        # upcoming semester buttons
        ttk.Label(input_frame, text="Upcoming Semester:", style="Custom.TLabel").grid(row=4, column=0, sticky=W, pady=(10, 5))
        
        upcoming_semester = ttk.Frame(input_frame)
        upcoming_semester.grid(row=4, column=1, sticky=W, pady=(10, 5))

        self.upcoming_semester_var = ttk.StringVar(value="Fall")
        self.upcoming_semester_buttons = {}

        for upcomingSemester in ["Fall", "Spring", "Summer"]:
            btn = ttk.Button(upcoming_semester, text=upcomingSemester, style="Semester.TButton", 
                            command=lambda s=upcomingSemester: self.select_semester(s))
            btn.pack(side=LEFT, padx=2)
            self.upcoming_semester_buttons[upcomingSemester] = btn

        self.update_button_states()

        ttk.Label(input_frame, text="Desired Credit Hours:", style="Custom.TLabel").grid(row=5, column=0, sticky=W, pady=(10, 5))
        self.credits_entry = ttk.Entry(input_frame, width=10, style="Custom.TEntry")
        self.credits_entry.grid(row=5, column=1, sticky=W, pady=(10, 5))

        # Course Completion Meter
        meter_frame = ttk.LabelFrame(content_frame, text="Course Completion Progress", padding="10")
        meter_frame.pack(side=RIGHT, padx=20, pady=20)

        self.completion_meter = ttk.Meter(
            meter_frame,
            metersize=180,
            padding=5,
            amountused=0,
            metertype="full",
            textright='%',
            subtext="Courses Completed",
            interactive=False,
        )
        self.completion_meter.pack(padx=10, pady=10)

        schedule_button = ttk.Button(main_frame, text="Generate Schedule", command=self.generate_schedule, style="Custom.TButton")
        schedule_button.pack(pady=20)

        # this is the chart that displays schedule
        self.results_notebook = ttk.Notebook(main_frame, height=400)
        self.results_notebook.pack(fill=BOTH, expand=YES, pady=10, padx=20)
        self.results_notebook.pack_forget()  # Hide initially

        # chart tabs
        self.recommended_tab = ttk.Frame(self.results_notebook)
        self.eligible_tab = ttk.Frame(self.results_notebook)
        self.ineligible_tab = ttk.Frame(self.results_notebook)

        self.results_notebook.add(self.recommended_tab, text="Recommended Classes")
        self.results_notebook.add(self.eligible_tab, text="Eligible Classes")
        self.results_notebook.add(self.ineligible_tab, text="Ineligible Classes")

        # scrolled frames
        self.recommended_scrolled = ScrolledFrame(self.recommended_tab)
        self.recommended_scrolled.pack(fill=BOTH, expand=YES)

        self.eligible_scrolled = ScrolledFrame(self.eligible_tab)
        self.eligible_scrolled.pack(fill=BOTH, expand=YES)

        self.ineligible_scrolled = ScrolledFrame(self.ineligible_tab)
        self.ineligible_scrolled.pack(fill=BOTH, expand=YES)

    def show_available_classes(self):
        popup = ttk.Toplevel(self)
        popup.title("Class List")
        popup.geometry("400x300")

        text_area = ScrolledText(popup, wrap='word', width=50, height=15)
        text_area.pack(expand=True, fill='both', padx=10, pady=10)

        for course in Courses:
            text_area.insert('end', f"{course.name}: {course.title}\n")
        
        text_area.configure(state='disabled')  # read-only

    def generate_schedule(self):
        name = self.name_entry.get()
        major = self.major_entry.get()
        completed_classes = [(c.strip()).upper() for c in self.completed_entry.get().split(',')]
        Completed_Class_Count = len(completed_classes)
        upcoming_semester = self.upcoming_semester_var.get()
        
        # desired hours error handling
        credits_input = self.credits_entry.get().strip()
        if not credits_input:
            desired_credits = 12
            self.credits_entry.delete(0, END)
            self.credits_entry.insert(0, "12")
            Messagebox.show_info("Desired Hours Defaulted to 12", "No input for Desired Credit Hours. Using default value of 12.")
        else:
            try:
                desired_credits = int(credits_input)
            except ValueError:
                desired_credits = 12
                self.credits_entry.delete(0, END)
                self.credits_entry.insert(0, "12")
                Messagebox.show_info("Desired Hours Defaulted to 12", "Invalid input for Desired Credit Hours. Using default value of 12.")

        # meter error handling
        if completed_classes == ['']:
            Completed_Class_Count = 0
        
        student = Student(name, major)
        student.completedCourses = completed_classes
        student.upcomingSemester = upcoming_semester

        eligible, ineligible = listOfEligibleCourses(Courses, upcoming_semester, completed_classes)

        # dataframes
        eligible_df = pd.DataFrame(eligible, columns=['Class', 'Importance', 'Semester Offered'])
        ineligible_df = pd.DataFrame(ineligible, columns=['Class', 'Prerequisites', 'Semester Offered'])

        # this orders by importance, but we can probably remove this. not sure if the user needs to know about our importance system
        eligible_df = eligible_df.sort_values('Importance', ascending=False) 

        selected_courses = []
        total_credits = 0
        # Adjust below, attempt to better fit desired hours (tries to avoid being 1-2 hours short)
        for _, course in eligible_df.iterrows():
            course_obj = next((c for c in Courses if c.name == course['Class']), None)
            if course_obj and total_credits + course_obj.credits <= desired_credits:
                selected_courses.append(course_obj)
                total_credits += course_obj.credits

        self.update_meter(Completed_Class_Count)
        #print(Completed_Class_Count)

        self.display_results(name, major, upcoming_semester, selected_courses, eligible_df, ineligible_df, total_credits)

        self.show_custom_popup() # custom popup

    def display_results(self, name, major, upcoming_semester, recommended_courses, eligible_df, ineligible_df, total_credits):
        # Show the results notebook if it's hidden
        if not self.results_visible:
            self.results_notebook.pack(fill=BOTH, expand=YES, pady=10, padx=20)
            self.results_visible = True

        # Clear previous results
        for widget in self.recommended_scrolled.winfo_children():
            widget.destroy()
        for widget in self.eligible_scrolled.winfo_children():
            widget.destroy()
        for widget in self.ineligible_scrolled.winfo_children():
            widget.destroy()

        # Display recommended courses 
        recommended_frame = ttk.Frame(self.recommended_scrolled)
        recommended_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(recommended_frame, text=f"Schedule for {name} ({major})", style="Title.TLabel").pack(pady=10)
        ttk.Label(recommended_frame, text=f"Upcoming Semester: {upcoming_semester}", style="Custom.TLabel").pack(pady=5)

        for course in recommended_courses:
            course_frame = ttk.Frame(recommended_frame, style="TFrame", padding=5)
            course_frame.pack(fill=X, pady=2)
            ttk.Label(course_frame, text=f"{course.name}: {course.title}", style="Custom.TLabel").pack(side=LEFT)
            ttk.Label(course_frame, text=f"({course.credits} credits)", style="Custom.TLabel").pack(side=RIGHT)

        ttk.Label(recommended_frame, text=f"Total Credits: {total_credits}", style="Custom.TLabel").pack(pady=10)

        # Display eligible courses
        self.create_expandable_frame(self.eligible_scrolled, "Eligible & Available Classes", eligible_df)

        # Display ineligible courses
        self.create_expandable_frame(self.ineligible_scrolled, "Not Eligible/Available Classes", ineligible_df)

    def create_expandable_frame(self, parent, title, dataframe):
            frame = ttk.Frame(parent, style="TFrame")
            frame.pack(fill=X, pady=10)

            def toggle_content():
                if content_frame.winfo_viewable():
                    content_frame.pack_forget()
                    toggle_button.configure(text="▼ " + title)
                else:
                    content_frame.pack(fill=X)
                    toggle_button.configure(text="▲ " + title)

            toggle_button = ttk.Button(frame, text="▼ " + title, command=toggle_content, style="Custom.TButton")
            toggle_button.pack(fill=X)

            content_frame = ttk.Frame(frame, style="TFrame")
        
            for _, row in dataframe.iterrows():
                row_frame = ttk.Frame(content_frame, style="TFrame")
                row_frame.pack(fill=X, pady=2)
                for col, value in row.items():
                    ttk.Label(row_frame, text=str(value), style="Custom.TLabel").pack(side=LEFT, padx=5)

    # funny monkey
    def show_custom_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
        
        self.popup_window = ttk.Toplevel(self)
        self.popup_window.title("Schedule Generated")
        self.popup_window.geometry("300x200")

        label = ttk.Label(self.popup_window, text="Your class schedule has been successfully generated!", wraplength=250, justify="center")
        label.pack(pady=10)

        gif_url = "https://media.tenor.com/29Oitn7fy8UAAAAi/btd6-monkey.gif"
        response = requests.get(gif_url)
        img = Image.open(BytesIO(response.content))

        desired_width = 100  
        width_percent = (desired_width / float(img.size[0]))
        desired_height = int((float(img.size[1]) * float(width_percent)))

        frames = []

        try:
            while True:
                resized_img = img.copy()
                resized_img.thumbnail((desired_width, desired_height), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(resized_img))
                img.seek(len(frames))
        except EOFError:
            pass

        gif_label = ttk.Label(self.popup_window)
        gif_label.pack()

        def update_frame(frame_num):
            frame = frames[frame_num]
            gif_label.configure(image=frame)
            frame_num = (frame_num + 1) % len(frames)
            self.popup_window.after(50, update_frame, frame_num)

        update_frame(0)

        # Close the popup after 2 seconds
        threading.Timer(2.0, self.close_popup).start()

    def close_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def select_semester(self, upcomingSemester):
        self.upcoming_semester_var.set(upcomingSemester)
        self.update_button_states()

    def update_button_states(self):
        selected = self.upcoming_semester_var.get()
        for semester, button in self.upcoming_semester_buttons.items():
            if semester == selected:
                button.configure(style="Semester.Selected.TButton")
            else:
                button.configure(style="Semester.TButton")

    # Course Completion Meter (work in progress)
    def update_meter(self, Completed_Class_Count):

        total = 41
        completed = Completed_Class_Count
        if total > 0:
            percentage = (completed / total) * 100
            percentage_int = int(percentage)
            self.completion_meter.configure(amountused=percentage_int)
            self.completion_meter.configure(subtext=f"{completed}/{total} Courses")
        #print(Completed_Class_Count)
    

if __name__ == "__main__":
    app = MAPSScheduler()

    # Custom styles for semester buttons
    app.style.configure("Semester.TButton", padding = 5, width = 10)
    app.style.configure("Semester.Selected.TButton", padding=5, width=10, background="#00ff51", foreground="black", font=("Helvetica", 12, "bold"))
    

    app.mainloop()


