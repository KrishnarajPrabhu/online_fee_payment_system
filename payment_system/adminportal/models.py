from django.db import models


class login(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.name} {self.email} {self.password} {self.phone}"


class Computer_Science_and_Engineering(models.Model):
    student_ID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.student_ID} {self.name}"


class Information_Science_and_Engineering(models.Model):

    student_ID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.student_ID} {self.name}"


class Course(models.Model):
    course_ID = models.CharField(max_length=50, primary_key=True)
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course_ID} {self.course_name}"
