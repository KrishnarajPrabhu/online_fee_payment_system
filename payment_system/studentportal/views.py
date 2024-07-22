from django.shortcuts import render
import datetime
from adminportal.models import Computer_Science_and_Engineering, Information_Science_and_Engineering

def dashboard(request):
    today = datetime.datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    student = Computer_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if not student:
        student = Information_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if student:
        name = student.name
    else:
        name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request, 'studentportal/student_dash.html', context)

def payment(request):
    today = datetime.datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    student = Computer_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if not student:
        student = Information_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if student:
        name = student.name
    else:
        name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request, 'studentportal/student_payment.html', context)

def queries(request):
    today = datetime.datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    student = Computer_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if not student:
        student = Information_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if student:
        name = student.name
    else:
        name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request,'studentportal/student_queries.html', context)

def acc_settings(request):
    today = datetime.datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    student = Computer_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if not student:
        student = Information_Science_and_Engineering.objects.filter(student_ID=student_ID).first()
    if student:
        name = student.name
    else:
        name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request,'studentportal/student_settings.html', context)