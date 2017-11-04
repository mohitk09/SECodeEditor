from django import forms
from .models import FacultyCourseSectionRelation
from .models import Faculty

class LoginCredentials(forms.Form):
    user_name = forms.CharField(label='UserName', max_length=30, widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.TextInput(attrs={'class': 'password'}))


class AddProblem(forms.Form):
    faculty_data = Faculty.objects.get(Id='1')
    faculty_course_section = FacultyCourseSectionRelation.objects.filter(FacultyId__Id='1')

    course = []
    section = []

    i = 0
    j = 0

    for cs in faculty_course_section:
        if cs.CourseId.Name not in course:
            course.append((cs.CourseId.Name, cs.CourseId.Name))
            i += 1
        if cs.SectionId.SectionId not in section:
            section.append((cs.SectionId.SectionId, cs.SectionId.SectionId))
            j += 1

    problem_name = forms.CharField(label='problem_name', max_length='50')
    course = forms.ChoiceField(choices=course, initial='0', required=True, label='course', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'course'}))
    section = forms.ChoiceField(choices=section, required=True, label='section', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'section'}))
    start_time = forms.DateField(label='start_time')
    end_time = forms.DateField(label='end_time')
    max_marks = forms.IntegerField(label='max_marks')
    max_attempts = forms.IntegerField(label='max_attempts')
    '''
    languages = [('c_lang', 'c_lang'),
                 ('cpp_lang', 'cpp_lang'),
                 ('java_lang', 'java_lang'),
                 ('python_lang', 'python_lang')]

    language_choices = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=languages,
    )
    '''
    c_lang = forms.BooleanField(label='c_lang', required=False)
    cpp_lang = forms.BooleanField(label='cpp_lang', required=False)
    java_lang = forms.BooleanField(label='java_lang', required=False)
    python_lang = forms.BooleanField(label='python_lang', required=False)
    test_case_file = forms.FileField(label='test_case_file', required=True)
    problem_statement = forms.CharField(label='problem_statement', max_length='2000')
