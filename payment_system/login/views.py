from django.shortcuts import render, redirect
from django.contrib.auth import logout
from adminportal.models import login as logindb, Computer_Science_and_Engineering, Information_Science_and_Engineering
from django.contrib.auth.hashers import check_password


def login(request):
    context = {}
    context['is_error'] = False
    context['error'] = ''
    return render(request, 'login/login.html', context)


def do_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')


def login_validation(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        context = {}
        try:
            user = logindb.objects.get(email=email)
            if check_password(password, user.password):
                request.session['logged_in'] = True
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['phone'] = user.phone
                return redirect('/adm/dashboard/')
            else:
                context['is_error'] = True
                context['error'] = 'Invalid Username or Password'
                return render(request, 'login/login.html', context)
        except logindb.DoesNotExist:
            student_db_data = (
                Computer_Science_and_Engineering.objects.filter(email=email).first() or
                Information_Science_and_Engineering.objects.filter(
                    email=email).first()
            )
            if student_db_data and check_password(password, student_db_data.password):
                request.session['logged_in'] = True
                request.session['ID'] = student_db_data.student_ID
                return redirect('/stu/dashboard/')
            else:
                context['is_error'] = True
                context['error'] = 'Invalid Username or Password'
                return render(request, 'login/login.html', context)


"""
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from adminportal.models import login as logindb, Computer_Science_and_Engineering, Information_Science_and_Engineering


def login(request):
    context = {}
    context['is_error'] = False
    context['error'] = ''
    return render(request, 'login/login.html', context)


def do_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')


def login_validation(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        context = {}
        db_data = logindb.objects.all().values()
        if email == db_data[0]['email'] and password == db_data[0]['password']:
            request.session['logged_in'] = True
            request.session['name'] = db_data[0]['name']
            return redirect('/adm/dashboard/')
        student_db_data = ''
        student_db_data = Computer_Science_and_Engineering.objects.filter(
            email=email, password=password).values() or Information_Science_and_Engineering.objects.filter(email=email, password=password).values()
        if student_db_data:
            request.session['logged_in'] = True
            # Student_ID is stored in the session.
            request.session['ID'] = student_db_data[0]['student_ID']
            return redirect('/stu/dashboard/')
        else:
            context['is_error'] = True
            context['error'] = 'Invalid Username or Password'
            return render(request, 'login/login.html', context)
"""
