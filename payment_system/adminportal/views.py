from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from io import BytesIO
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Computer_Science_and_Engineering
from .models import Information_Science_and_Engineering
from .models import Course, Fees_details
from django.contrib.auth.hashers import make_password, check_password
import json
from django.contrib import messages
from .models import login as admindb

Model_Mapping = {
    'CSE01': Computer_Science_and_Engineering,
    'ISE02': Information_Science_and_Engineering
}

# for retuning admin dashboard(template)


def adm_dashboard(request):
    email = request.session['email']
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name': request.session['name'],
        'email' : email,
    }
    return render(request, 'adminportal/admin_dash.html', context)

# classes and students


def student_list(request):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name': request.session['name'],
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
            'name': request.session['name'],
        }
        return render(request, 'adminportal/admin_paymentsetup.html', context)
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name': request.session['name'],
    }
    return render(request, 'adminportal/admin_paymentsetup.html', context)

# payment history


def payment_history(request):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name': request.session['name'],
    }
    return render(request, 'adminportal/admin_paymenthistory.html', context)


# profile & settings

def adm_profile(request):  
    if request.method == 'POST':
        # Handle profile update
        if 'profile_update' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            admin = admindb.objects.get(email=request.session['email'])
            admin.name = name
            admin.email = email
            admin.phone = phone
            admin.save()
            
            # Update session data
            request.session['name'] = admin.name
            request.session['email'] = admin.email
            request.session['phone'] = admin.phone
            
            messages.success(request, 'Profile updated successfully!')
        
        # Handle password change
        elif 'password_change' in request.POST:
            old_password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            admin = admindb.objects.get(email=request.session['email'])
            
            if check_password(old_password, admin.password):
                if new_password == confirm_password:
                    admin.password = make_password(new_password)
                    admin.save()
                    messages.success(request, 'Password changed successfully!')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Old password is incorrect.')

        return redirect('adm_profile')

    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name': request.session['name'],
        'email': request.session['email'],
        'phone': request.session.get('phone', ''),
    }
    return render(request, 'adminportal/admin_profile.html', context)


# payment edit details

def payment_edit(request, id):
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_paymenteditdetails.html', context)

#payment details

def payment_details(request, payment_id):
    # Fetch payment details for the given ID
    context = {
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'name' : request.session['name'],
    }
    return render(request, 'adminportal/admin_paymentdetails.html', context)


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

        a = len(course_code) - 2
        cnt = 1

        for index, row in df.iterrows():
            value = row['student_ID']

            if value == ' ':
                return JsonResponse({'message': 'Student_ID is empty'}, status=400)

            for i in range(a):
                if course_code[i] != value[i + 2]:
                    return JsonResponse({'message': 'Student_ID did not match with course'}, status=400)

            if int(value[2 + a:]) != cnt:
                return JsonResponse({'message': 'Student_ID are not continuous'}, status=400)
            cnt = cnt + 1

            if row['name'] == ' ' or row['email'] == ' ' or row['password'] == ' ' or row['phone'] == ' ':
                return JsonResponse({'message': 'Fields cannot be empty'}, status=400)

            tble_name = Model_Mapping.get(course_code)

            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE {tble_name._meta.db_table};')

            # Hash the password before inserting into the database
            for index, row in df.iterrows():
                hashed_password = make_password(row['password'])
                tble_name.objects.create(
                    student_ID=row['student_ID'],
                    name=row['name'],
                    email=row['email'],
                    password=hashed_password,
                    phone=int(row['phone'])
                )

            return JsonResponse({'message': 'Details are uploaded successfully'}, status=200)


# This are funtionality that are related to payment.

@csrf_exempt
def Paid_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('paymentId')
        payment_data = Fees_details.objects.get(id=payment_id)
        course_code = payment_data.course_id
        payment_description = payment_data.description
        table_name = course_code+"_FD"

        print("I am called!")

        with connection.cursor() as cursor:

            print("Gm mahesh!")

            query = f'select count(*) from information_schema.tables where table_name="{table_name}"'
            cursor.execute(query)

            if cursor.fetchall()[0][0] == 0:

                print("Hello world")
                tble_name = Model_Mapping.get(course_code)
                student_ID = tble_name.objects.values_list(
                    'student_ID', flat=True)
                columns = ['Id int primary key, description varchar(255)']
                columns.extend(
                    [f'{student_id} varchar(255)' for student_id in student_ID])
                create_table_sql = f'create table {table_name} ({", ".join(columns)})'
                cursor.execute(create_table_sql)
                query = f"insert into {table_name} (Id, description) values ({payment_id}, '{payment_description}');"
                print(query)
                cursor.execute(query)
                cursor.execute(
                    f'update {Fees_details._meta.db_table} set status=1 where id={payment_id};')
            else:
                print("Gm")
                query = f"insert into {table_name} (Id, description) values ({payment_id}, '{payment_description}');"
                print(query)
                cursor.execute(query)
                cursor.execute(
                    f'update {Fees_details._meta.db_table} set status=1 where id={payment_id};')
            return JsonResponse("The course already started!", safe=False)
