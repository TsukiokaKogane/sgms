from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StudentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cls = models.CharField('class', max_length=15)


class TeacherInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CourseInfo(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField('course', max_length=15)


class ClassInfo(models.Model):
    cls = models.CharField('class', max_length=15)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE)


class StudentCourse(models.Model):
    stu = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE)
    pt = models.DecimalField(max_digits=5, decimal_places=2)
