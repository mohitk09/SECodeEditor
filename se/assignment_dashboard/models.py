from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username + " " + self.role


class Student(models.Model):
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    RegistrationId = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    Email_id = models.CharField(max_length=50)
    Year = models.CharField(max_length=4)
    NumberOfSuccessfulSubmission = models.IntegerField()

    def __str__(self):
        return self.Name


class Faculty(models.Model):
    Id = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    Email_id = models.CharField(max_length=50)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Course(models.Model):
    Name = models.CharField(max_length=30)
    Course_id = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.Name


class Section(models.Model):
    SectionId = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.SectionId


class StudentCourseRelation(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.Student.Name + " " + self.Course.Name


class StudentSectionRelation(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.Student.Name + " " + self.Section.SectionId


class FacultyCourseSectionRelation(models.Model):
    Faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    Batch = models.CharField(max_length=4)

    def __str__(self):
        return self.Faculty.Name + " " + self.Course.Name + " " + self.Section.SectionId + " " + self.Batch


class Problem(models.Model):
    Problem = models.AutoField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    startDate = models.DateField()
    endDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    maxMarks = models.IntegerField()
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    ProblemStatement = models.CharField(max_length=10000)
    maxAttempts = models.IntegerField()
    test_case_file = models.FileField(upload_to='D:/xampp/htdocs/se/Test_Case_File_Uploads/')
    Faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


    def __str__(self):
        return self.Name + " " + " " + self.Faculty.Name + self.Course.Name + " " + self.Section.SectionId


class ProblemLanguages(models.Model):
    Problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    Language = models.CharField(max_length=10)

    def __str__(self):
        return self.Problem.Name + " " + self.Language


class StudentProblemRelation(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    attempt = models.IntegerField()

    def __str__(self):
        return self.Student.Name + " " + self.Problem.Name


class Solution(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    attempt = models.IntegerField()
    DateTime = models.DateTimeField()
    UserFileName = models.CharField(max_length=50)
    UserFileNameUnique = models.CharField(max_length=50)
    Status = models.CharField(max_length=10)
    Marks = models.IntegerField()
    LanguageUsed = models.CharField(max_length=10)

    def __str__(self):
        return self.Student.Name + " " + self.Problem.Name + " " +self.Status
