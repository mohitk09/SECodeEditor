from django import forms
from .models import FacultyCourseSectionRelation
from .models import Faculty
from .models import Users

class LoginCredentials(forms.Form):
    user_name = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'password'}))


class AddProblem(forms.Form):

    courses=[]
    sections = []

    def __init__(self, *args, **kwargs):
        global courses
        global sections
        user = kwargs.pop('user')
        super(AddProblem, self).__init__(*args, **kwargs)
        users = Users.objects.get(user=user)
        faculty = Faculty.objects.get(User=users)
        fcsr = FacultyCourseSectionRelation.objects.filter(Faculty=faculty)

        for cs in fcsr:
            if (cs.Course.Name, cs.Course.Name) not in self.courses:
                self.courses.append((cs.Course.Name, cs.Course.Name))
            if (cs.Section.SectionId, cs.Section.SectionId) not in self.sections:
                self.sections.append((cs.Section.SectionId, cs.Section.SectionId))

        self.fields['section'] = forms.ChoiceField(choices=self.sections, required=True, label='section', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'section'}))
        self.fields['course'] = forms.ChoiceField(choices=self.courses, required=True, label='course', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'course'}))


    problem_name = forms.CharField(label='problem_name', max_length='50')
    course = forms.ChoiceField(choices=courses, required=True, label='course', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'course'}))
    section = forms.ChoiceField(choices=sections, required=True, label='section', widget=forms.Select(attrs={'class': 'sort-select', 'id': 'section'}))
    start_date = forms.DateField(label='start_date')
    end_date = forms.DateField(label='end_date')
    start_time = forms.TimeField(label='start_time')
    end_time = forms.TimeField(label='end_time')
    max_marks = forms.IntegerField(label='max_marks')
    max_attempts = forms.IntegerField(label='max_attempts')
    c_lang = forms.BooleanField(label='c_lang', required=False)
    cpp_lang = forms.BooleanField(label='cpp_lang', required=False)
    java_lang = forms.BooleanField(label='java_lang', required=False)
    python_lang = forms.BooleanField(label='python_lang', required=False)
    test_case_file = forms.FileField(label='test_case_file', required=True)
    problem_statement = forms.CharField(label='problem_statement', max_length='2000')


