from django.db import models


class login(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.name} {self.email} {self.password} {self.phone}"


class Computer_Science_and_Engineering(models.Model):
    student_ID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.student_ID} {self.name}"


class Information_Science_and_Engineering(models.Model):

    student_ID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.student_ID} {self.name}"


class Course(models.Model):
    course_ID = models.CharField(max_length=50, primary_key=True)
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course_ID} {self.course_name}"


# Just created to store the fees details
class Fees_details(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    amount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} {self.description} {self.amount} {self.start_date} {self.end_date}"
