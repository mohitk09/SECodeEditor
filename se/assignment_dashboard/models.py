from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=10)


class Student(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    RegistrationId = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    Email_id = models.CharField(max_length=50)
    Year = models.CharField(max_length=4)
    NumberOfSuccessfulSubmission = models.IntegerField()


class Faculty(models.Model):
    Id = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    Email_id = models.CharField(max_length=50)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    Name = models.CharField(max_length=30)
    Course_id = models.CharField(max_length=10, primary_key=True)


class Section(models.Model):
    SectionId = models.CharField(max_length=10, primary_key=True)


class StudentCourseRelation(models.Model):
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    CourseId = models.ForeignKey(Course, on_delete=models.CASCADE)


class StudentSectionRelation(models.Model):
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    SectionId = models.ForeignKey(Section, on_delete=models.CASCADE)


class FacultyCourseSectionRelation(models.Model):
    FacultyId = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    CourseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    SectionId = models.ForeignKey(Section, on_delete=models.CASCADE)
    Batch = models.CharField(max_length=4)


class Problem(models.Model):
    ProblemId = models.AutoField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=30)
    startDate = models.DateField()
    endDate = models.DateField()
    maxMarks = models.IntegerField()
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE)
    ProblemStatement = models.CharField(max_length=10000)
    maxAttempts = models.IntegerField()
    test_case_file = models.FileField(upload_to='D:/xampp/htdocs/se/Test_Case_File_Uploads/')


class ProblemLanguages(models.Model):
    ProblemId = models.ForeignKey(Problem, on_delete=models.CASCADE)
    Language = models.CharField(max_length=10)


class StudentProblemRelation(models.Model):
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    ProblemId = models.ForeignKey(Problem, on_delete=models.CASCADE)
    attempt = models.IntegerField()


class Solution(models.Model):
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    ProblemId = models.ForeignKey(Problem, on_delete=models.CASCADE)
    attempt = models.IntegerField()
    DateTime = models.DateTimeField()
    UserFileName = models.CharField(max_length=50)
    UserFileNameUnique = models.CharField(max_length=50)
    Status = models.CharField(max_length=10)
    Marks = models.IntegerField()
    LanguageUsed = models.CharField(max_length=10)
