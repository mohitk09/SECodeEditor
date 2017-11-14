from django.contrib import admin
from .models import Users
from .models import Student
from .models import Faculty
from .models import Course
from .models import Section
from .models import StudentCourseRelation
from .models import StudentSectionRelation
from .models import FacultyCourseSectionRelation
from .models import Problem
from .models import ProblemLanguages
from .models import StudentProblemRelation
from .models import Solution

# Register your models here.

admin.site.register(Users)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(StudentCourseRelation)
admin.site.register(StudentSectionRelation)
admin.site.register(FacultyCourseSectionRelation)
admin.site.register(Problem)
admin.site.register(ProblemLanguages)
admin.site.register(StudentProblemRelation)
admin.site.register(Solution)
