from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Users
from .models import Problem
from .models import StudentProblemRelation
from .models import Student
from .models import StudentSectionRelation
from .models import Solution
from .models import Faculty
from .models import FacultyCourseSectionRelation
from .models import Course
from .models import Section
from .models import ProblemLanguages
from .models import StudentCourseRelation

from .forms import LoginCredentials
from .forms import AddProblem

import datetime


def index_student(request):

    if request.user.is_authenticated():
        user = Users.objects.get(user=request.user)

        student_data = Student.objects.get(User=user)
        section = StudentSectionRelation.objects.get(Student__User=user)

        solution = Solution.objects.filter(Student__User=user)

        problems_total = Problem.objects.all()
        student_problem = StudentProblemRelation.objects.filter(Student__User=user)
        problem_student = []
        for x in student_problem:
            for problem in problems_total:
                if x.Problem.Problem == problem.Problem:
                    problem_student.append(problem)

        problem_sub = []
        problem_nsub = []
        solution_attempts = []
        for x in problem_student:
            for y in solution:
                if x.Problem == y.Problem.Problem:
                    problem_sub.append(x)
                    solution_attempts.append(y.attempt)
                else:
                    problem_nsub.append(x)

        if len(solution) == 0:
            problem_nsub = problem_student

        context = {
            'problems': problem_student,
            'problem_sub': problem_sub,
            'problem_nsub': problem_nsub,
            'student_data': student_data,
            'section': section,
            'problem_sub_sol': zip(problem_sub, solution_attempts),
        }
        return render(request, 'assignment_dashboard/student_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('assignment_dashboard:index_login'))


def index_faculty(request):

    if request.user.is_authenticated():
        user = Users.objects.get(user=request.user)
        faculty_data = Faculty.objects.get(User=user)
        faculty_course_section = FacultyCourseSectionRelation.objects.filter(Faculty__User=user)

        course_section = {}

        for cs in faculty_course_section:
            if cs.Course not in course_section:
                course_section[cs.Course] = [cs.Section]
            else:
                course_section[cs.Course] += [cs.Section]

        context = {
            'faculty_data': faculty_data,
            'course_section': course_section,
        }
        return render(request, 'assignment_dashboard/faculty_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('assignment_dashboard:index_login'))


def add_problem(request):
    if request.user.is_authenticated():
        user = Users.objects.get(user=request.user)
        faculty_data = Faculty.objects.get(User=user)
        faculty_course_section = FacultyCourseSectionRelation.objects.filter(Faculty=faculty_data)
        course_section = {}
        courses = []
        sections = []

        for cs in faculty_course_section:

            if cs.Course.Name not in courses:
                courses.append(cs.Course.Name)
            if cs.Section.SectionId not in sections:
                sections.append(cs.Section.SectionId)

            if cs.Course not in course_section:
                course_section[cs.Course] = [cs.Section]
            else:
                course_section[cs.Course] += [cs.Section]

        context = {
            'faculty_data': faculty_data,
            'course_section': course_section,
            'courses': courses,
            'sections': sections,
        }

        if request.method == 'POST':
            form = AddProblem(request.POST, request.FILES, user=request.user)
            print("datetime= " + str(datetime.datetime.now()))
            if form.is_valid():

                problem_name = request.POST['problem_name']
                course = request.POST['course']
                section = request.POST['section']
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                max_marks = request.POST['max_marks']
                max_attempts = request.POST['max_attempts']
                c = "unchecked"
                cpp = "unchecked"
                java = "unchecked"
                python = "unchecked"
                try:
                    c = request.POST['c_lang']
                except MultiValueDictKeyError:
                    pass
                try:
                    cpp = request.POST['cpp_lang']
                except MultiValueDictKeyError:
                    pass
                try:
                    java = request.POST['java_lang']
                except MultiValueDictKeyError:
                    pass
                try:
                    python = request.POST['python_lang']
                except MultiValueDictKeyError:
                    pass

                problem_statement = request.POST['problem_statement']
                test_case_file = request.FILES['test_case_file']

                course_d = Course.objects.get(Name=course)
                section_d = Section.objects.get(SectionId=section)

                print(datetime.datetime.now().date())

                start_date_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                print(start_date_datetime)
                print(end_date_datetime)

                if start_date_datetime >= datetime.datetime.now().date():
                    if end_date_datetime >= datetime.datetime.now().date() and end_date_datetime >=start_date_datetime:
                        if (start_date_datetime == end_date_datetime and end_time > start_time) or end_date_datetime > start_date_datetime:
                            new_problem = Problem.objects.create(Name=problem_name, startDate=start_date, endDate=end_date, startTime=start_time, endTime=end_time, maxMarks=max_marks, Course=course_d, Section=section_d, ProblemStatement=problem_statement, maxAttempts=max_attempts, test_case_file=test_case_file,Faculty=faculty_data)
                            new_problem.save()

                            if c is not "unchecked":
                                problem_language_entry_c = ProblemLanguages.objects.create(Problem=new_problem, Language="C")
                                problem_language_entry_c.save()
                            if cpp is not "unchecked":
                                problem_language_entry_cpp = ProblemLanguages.objects.create(Problem=new_problem, Language="C++")
                                problem_language_entry_cpp.save()
                            if java is not "unchecked":
                                problem_language_entry_java = ProblemLanguages.objects.create(Problem=new_problem, Language="Java")
                                problem_language_entry_java.save()
                            if python is not "unchecked":
                                problem_language_entry_python = ProblemLanguages.objects.create(Problem=new_problem, Language="Python")
                                problem_language_entry_python.save()

                            students_with_course = StudentCourseRelation.objects.filter(Course=course_d)

                            for student in students_with_course:
                                try:
                                    print(student.Student.Name + section_d.SectionId)
                                    student_s = StudentSectionRelation.objects.get(Student=student.Student, Section=section_d)
                                    s = StudentProblemRelation.objects.create(Student=student_s.Student, Problem=new_problem, attempt=0)
                                    s.save()
                                except StudentSectionRelation.DoesNotExist:
                                    pass

                            # handle_uploaded_file(request.FILES['test_case_file'], 'name2.txt')
                            messages.success(request, "Problem " + problem_name + " successfully allocated to students of " + course + " " + section +" batch "+ "2015")
                            return HttpResponseRedirect(reverse('assignment_dashboard:index_faculty'))
                        else:
                            messages.error(request, "End time should be greater than start time.")
                    else:
                        messages.error(request, "End date should be greater than current and start date.")
                else:
                    messages.error(request, "Start date should be greater than current date.")
            else:
                print(" errors " + str(form.errors) + "\n\n")
                print(" non field errors " + form.non_field_errors() + "\n\n")
                messages.error(request, "Please fill in all fields.\n")
        else:
            form = AddProblem(user=request.user)
            context['form'] = form
            return render(request, 'assignment_dashboard/add_problem.html', context)
        return render(request, 'assignment_dashboard/add_problem.html', context)
    else:
        return HttpResponseRedirect(reverse('assignment_dashboard:index_login'))


def index_login(request):
    if request.method == 'POST':
        form = LoginCredentials(request.POST)
        user_name = request.POST['user_name']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(request, username=user_name, password=password)

            if user is not None:
                if user.is_active:
                    user1 = Users.objects.get(user=user)
                    login(request, user)
                    print("user role="+str(user1.role))
                    if user1.role == "student":
                        return HttpResponseRedirect(reverse('assignment_dashboard:index_student'))
                    else:
                        return HttpResponseRedirect(reverse('assignment_dashboard:index_faculty'))
                else:
                    messages.error(request, "The account is temporarily deactivated.")
            else:
                messages.error(request, "Wrong username or password")
        else:
            form = LoginCredentials()
            return render(request, 'assignment_dashboard/login.html', {'form': form})
    else:
        form = LoginCredentials()
    return render(request, 'assignment_dashboard/login.html', {'form': form})


def handle_uploaded_file(f, file_name):
    with open('D:/xampp/htdocs/se/Test_Case_File_Uploads/'+file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('assignment_dashboard:index_login'))

def problems(request):
    if request.user.is_authenticated():
        user = Users.objects.get(user=request.user)
        faculty_data = Faculty.objects.get(User=user)
        faculty_course_section = FacultyCourseSectionRelation.objects.filter(Faculty__User=user)

        problems_added = Problem.objects.filter(Faculty=faculty_data)


        course_section = {}

        for cs in faculty_course_section:
            if cs.Course not in course_section:
                course_section[cs.Course] = [cs.Section]
            else:
                course_section[cs.Course] += [cs.Section]

        context = {
            'faculty_data': faculty_data,
            'problems_added': problems_added,
        }
        return render(request, 'assignment_dashboard/problems.html', context)
    else:
        return HttpResponseRedirect(reverse('assignment_dashboard:index_login'))
