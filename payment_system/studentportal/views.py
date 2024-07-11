from django.shortcuts import render
import datetime


def dashboard(request):
    today = datetime.datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    context = {}
    context['current_date'] = current_date
    context['student_ID'] = request.session['ID']
    return render(request, 'studentportal/student_dash.html', context)
