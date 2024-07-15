from django.shortcuts import render
from datetime import datetime
from io import BytesIO
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Computer_Science_and_Engineering
from .models import Information_Science_and_Engineering
from .models import Course, Fees_details

Model_Mapping = {
    'CSE01': Computer_Science_and_Engineering,
    'ISE02': Information_Science_and_Engineering
}

# for retuning admin dashboard(template)


def adm_dashboard(request):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_dash.html', context)

# classes and students


def student_list(request):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_studentlist.html', context)

# fee payment setup


def payment_setup(request):
    if request.method == "POST":
        course_ID = request.POST['choice']
        description = request.POST['feeName']
        amount = request.POST['amount']
        start_date = request.POST['startDate']
        end_date = request.POST['dueDate']

        Fees_details.objects.create(
            course_id=course_ID,
            description=description,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            status=0
        )
        context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
        return render(request, 'adminportal/admin_paymentsetup.html', context)
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_paymentsetup.html', context)

# payment history


def payment_history(request):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_paymenthistory.html', context)

# API that sends course details -> The course that are present in the college.


def course(request):
    course = Course.objects.all().values('course_name', 'course_ID')
    data = list(course)
    return JsonResponse(data, safe=False)

# API to get the course details assigned to the student by the admin.


def get_Fees_details(request):
    db_fees_details = Fees_details.objects.all().values(
        'id', 'description', 'course_id', 'amount', 'start_date', 'end_date', 'status')
    print(db_fees_details)
    data = list(db_fees_details)
    return JsonResponse(data, safe=False)


# To get the student details
@csrf_exempt
def studentDetails(request):
    course_code = request.POST.get('choice')
    tble_name = Model_Mapping.get(course_code)
    student = tble_name.objects.all().values(
        'student_ID', 'name', 'phone', 'email')
    data = list(student)
    return JsonResponse(data, safe=False)


# To add the student details from the Excel fiel into the database.
@csrf_exempt
def addStudent(request):
    if request.method == 'POST':
        course_code = request.POST.get('choice')
        excel_file = request.FILES['file']
        df = pd.read_excel(BytesIO(excel_file.read()), engine='openpyxl')

        a = len(course_code)-2
        cnt = 1

        for index, row in df.iterrows():

            value = row['student_ID']

            if value == ' ':
                return JsonResponse({'message': 'Student_ID is empty'}, status=400)

            for i in range(a):
                if course_code[i] != value[i+2]:
                    return JsonResponse({'message': 'Student_ID did not match with course'}, status=400)

            if int(value[2+a:]) != cnt:
                return JsonResponse({'message': 'Student_ID are not continouse'}, status=400)
            cnt = cnt+1

            if row['name'] == ' ' or row['email'] == ' ' or row['password'] == ' ' or row['phone'] == ' ':
                return JsonResponse({'message': 'Fiels cannot be empty'},  status=400)

            tble_name = Model_Mapping.get(course_code)

            with connection.cursor() as cursor:
                cursor.execute(
                    f'TRUNCATE TABLE {tble_name._meta.db_table};')

            for index, row in df.iterrows():
                tble_name.objects.create(
                    student_ID=row['student_ID'],
                    name=row['name'],
                    email=row['email'],
                    password=row['password'],
                    phone=int(row['phone'])
                )
            return JsonResponse({'message': 'Details are uploaded successfully'}, status=200)


# This are funtionality that are related to payment.

def Paid_details(request, value):
    # course_code = request.POST.get('choice')
    course_code = value
    table_name = course_code+"_FD"

    with connection.cursor() as cursor:
        query = f'select count(*) from information_schema.tables where table_name="{table_name}"'
        print(query)
        cursor.execute(query)
        if cursor.fetchone()[0] == 1:
            return JsonResponse("The course already started!", safe=False)

    tble_name = Model_Mapping.get(value)
    student_ID = tble_name.objects.values_list('student_ID', flat=True)
    columns = ['Id int primary key, description varchar(255)']
    columns.extend([f'{student_id} varchar(255)' for student_id in student_ID])
    create_table_sql = f'create table {table_name} ({", ".join(columns)})'
    print(create_table_sql)
    with connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        cursor.execute(create_table_sql)
    return JsonResponse("Table is successfully created", safe=False)
