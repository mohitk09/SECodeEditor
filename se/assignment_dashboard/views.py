from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse

from .models import User
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


def index_student(request, pk):

    reg_id = Student.objects.get(UserId=pk).RegistrationId;
    student_data = Student.objects.get(RegistrationId=reg_id)
    section = StudentSectionRelation.objects.get(StudentId__RegistrationId=reg_id)

    solution = Solution.objects.filter(StudentId__RegistrationId=reg_id)





    problems_total = Problem.objects.all()
    student_problem = StudentProblemRelation.objects.filter(StudentId__RegistrationId=reg_id)
    problem_student = []
    for x in student_problem:
        for problem in problems_total:
            if x.ProblemId.ProblemId == problem.ProblemId:
                problem_student.append(problem)

    problem_sub = []
    problem_nsub = []
    solution_attempts = []
    for x in problem_student:
        for y in solution:
            if x.ProblemId == y.ProblemId.ProblemId:
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


def index_faculty(request, pk):

    faculty_id = Faculty.objects.get(UserId=pk).Id

    faculty_data = Faculty.objects.get(Id=faculty_id)
    faculty_course_section = FacultyCourseSectionRelation.objects.filter(FacultyId__Id=faculty_id)

    course_section = {}

    for cs in faculty_course_section:
        if cs.CourseId not in course_section:
            course_section[cs.CourseId] = [cs.SectionId]
        else:
            course_section[cs.CourseId] += [cs.SectionId]

    context = {
        'faculty_data': faculty_data,
        'course_section': course_section,
    }
    return render(request, 'assignment_dashboard/faculty_dashboard.html', context)


def add_problem(request):
    faculty_data = Faculty.objects.get(Id='1')
    faculty_course_section = FacultyCourseSectionRelation.objects.filter(FacultyId__Id='1')

    course_section = {}
    courses = []
    sections = []

    for cs in faculty_course_section:

        if cs.CourseId.Name not in courses:
            courses.append(cs.CourseId.Name)
        if cs.SectionId.SectionId not in sections:
            sections.append(cs.SectionId.SectionId)

        if cs.CourseId not in course_section:
            course_section[cs.CourseId] = [cs.SectionId]
        else:
            course_section[cs.CourseId] += [cs.SectionId]

    context = {
        'faculty_data': faculty_data,
        'course_section': course_section,
        'courses': courses,
        'sections': sections,
    }

    if request.method == 'POST':
        form = AddProblem(request.POST, request.FILES)
        if form.is_valid():

            problem_name = request.POST['problem_name']
            course = request.POST['course']
            section = request.POST['section']
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
            new_problem = Problem.objects.create(Name=problem_name, startDate=start_time, endDate=end_time, maxMarks=max_marks, Course=course_d, Section=section_d, ProblemStatement=problem_statement, maxAttempts=max_attempts, test_case_file=test_case_file)
            new_problem.save()

            if c is not "unchecked":
                problem_language_entry_c = ProblemLanguages.objects.create(ProblemId=new_problem, Language="C")
                problem_language_entry_c.save()
            if cpp is not "unchecked":
                problem_language_entry_cpp = ProblemLanguages.objects.create(ProblemId=new_problem, Language="C++")
                problem_language_entry_cpp.save()
            if java is not "unchecked":
                problem_language_entry_java = ProblemLanguages.objects.create(ProblemId=new_problem, Language="Java")
                problem_language_entry_java.save()
            if python is not "unchecked":
                problem_language_entry_python = ProblemLanguages.objects.create(ProblemId=new_problem, Language="Python")
                problem_language_entry_python.save()


            students_with_course = StudentCourseRelation.objects.filter(CourseId=course_d)

            for student in students_with_course:
                try:
                    print(student.StudentId.Name + section_d.SectionId)
                    student_s = StudentSectionRelation.objects.get(StudentId=student.StudentId, SectionId=section_d)
                    s = StudentProblemRelation.objects.create(StudentId=student_s.StudentId, ProblemId=new_problem, attempt=0)
                    s.save()
                except StudentSectionRelation.DoesNotExist:
                    pass

             #handle_uploaded_file(request.FILES['test_case_file'], 'name2.txt')

            return HttpResponseRedirect(reverse('assignment_dashboard:index_faculty'))
        else:
            print(" errors " + str(form.errors) + "\n\n")
            print(" non field errors " + form.non_field_errors() + "\n\n")

            c = "unchecked"
            cpp = "unchecked"
            java = "unchecked"
            python = "unchecked"
            return HttpResponse("unsuccessful " +
                request.POST['problem_name'] + request.POST['course'] + request.POST['section'] + request.POST[
                    'start_time'] + request.POST['end_time'] + request.POST['max_marks'] + request.POST[
                    'max_attempts'] + request.POST['problem_statement'] + c + cpp + java + python)
    else:
        form = AddProblem()
        context['form'] = form
        return render(request, 'assignment_dashboard/add_problem.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginCredentials(request.POST)
        l = 0
        dot = 0
        digit = 0
        user_name = request.POST['user_name']
        password = request.POST['password']
        if form.is_valid():
            '''
            for c in user_name:
                if c.islower() and l != 1:
                    l = 1
                if c.isdigit() and digit != 1:
                    digit = 1
                if c == '.':
                    dot += 1
            if l == 1 and digit == 1 and dot == 2 and len(user_name) >= 8 and len(password) >= 1:
                request.session['user_name'] = user_name
                '''
            try:
                user = User.objects.get(username=user_name, password=password)
            except User.DoesNotExist:
                form = LoginCredentials()
                return render(request, 'assignment_dashboard/login1.html', {'form': form})
            user_role = user.role.lower()
            if user_role == "student":
                return redirect('assignment_dashboard:index_student', pk=user.pk)
            elif user_role == 'faculty':
                return redirect('assignment_dashboard:index_faculty', pk=user.pk)
            else:
                form = LoginCredentials()
                return render(request, 'assignment_dashboard/login.html', {'form': form})
        else:
            form = LoginCredentials()
            return render(request, 'assignment_dashboard/login.html', {'form': form})
    else:
        form = LoginCredentials()
    return render(request, 'assignment_dashboard/login.html', {'form': form})

def handle_uploaded_file(f,file_name):
    with open('D:/xampp/htdocs/se/Test_Case_File_Uploads/'+file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def forgot_password(request):
    return HttpResponse('')

'''
return HttpResponse("unsuccessful " +
                request.POST['problem_name'] + request.POST['course'] + request.POST['section'] + request.POST[
                    'start_time'] + request.POST['end_time'] + request.POST['max_marks'] + request.POST[
                    'max_attempts'] + request.POST['problem_statement'] + c + cpp + java + python)
'''
