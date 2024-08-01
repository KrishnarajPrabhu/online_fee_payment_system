from django.shortcuts import render
from datetime import datetime
from adminportal.models import Computer_Science_and_Engineering, Information_Science_and_Engineering
from adminportal.models import Course, Fees_details
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


# Import that are related to payment.
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.conf import settings
from django.utils.timezone import make_aware
from django.shortcuts import redirect
from django.contrib.sessions.models import Session

# Imports thar are related to email.
from django.core.mail import EmailMessage
import os

# Imports that are related to pdf creation
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

# This will hold amount that student has selected to pay.
amount_student_going_to_pay = int(0)

Model_Mapping = {
    'CSE01': Computer_Science_and_Engineering,
    'ISE02': Information_Science_and_Engineering
}


def dashboard(request):
    today = datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    try:
        cse_instance = Computer_Science_and_Engineering.objects.get(
            student_ID=student_ID)
        name = cse_instance.name
    except Computer_Science_and_Engineering.DoesNotExist:
        try:
            ise_instance = Information_Science_and_Engineering.objects.get(
                student_ID=student_ID)
            name = ise_instance.name
        except Information_Science_and_Engineering.DoesNotExist:
            name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request, 'studentportal/student_dash.html', context)


def payment(request):
    today = datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    try:
        cse_instance = Computer_Science_and_Engineering.objects.get(
            student_ID=student_ID)
        name = cse_instance.name
    except Computer_Science_and_Engineering.DoesNotExist:
        try:
            ise_instance = Information_Science_and_Engineering.objects.get(
                student_ID=student_ID)
            name = ise_instance.name
        except Information_Science_and_Engineering.DoesNotExist:
            name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request, 'studentportal/student_payment.html', context)


def queries(request):
    today = datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    try:
        cse_instance = Computer_Science_and_Engineering.objects.get(
            student_ID=student_ID)
        name = cse_instance.name
    except Computer_Science_and_Engineering.DoesNotExist:
        try:
            ise_instance = Information_Science_and_Engineering.objects.get(
                student_ID=student_ID)
            name = ise_instance.name
        except Information_Science_and_Engineering.DoesNotExist:
            name = student_ID
    context = {
        'current_date': current_date,
        'student_ID': request.session['ID'],
        'name': name,
    }
    return render(request, 'studentportal/student_queries.html', context)

#profile-settings
def acc_settings(request):
    today = datetime.now()
    current_date = today.strftime('%d-%m-%Y')
    student_ID = request.session['ID']
    
    if request.method == 'POST':
        if 'profile_update' in request.POST:
            # Update email and phone
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            try:
                student = Computer_Science_and_Engineering.objects.get(student_ID=student_ID)
            except Computer_Science_and_Engineering.DoesNotExist:
                student = Information_Science_and_Engineering.objects.get(student_ID=student_ID)
            
            student.email = email
            student.phone = phone
            student.save()
            messages.success(request, 'Profile updated successfully!')
        
        elif 'password_change' in request.POST:
            # Change password
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            reenter_password = request.POST.get('reenter_password')
            try:
                student = Computer_Science_and_Engineering.objects.get(student_ID=student_ID)
            except Computer_Science_and_Engineering.DoesNotExist:
                student = Information_Science_and_Engineering.objects.get(student_ID=student_ID)
            
            if check_password(old_password, student.password):
                if new_password == reenter_password:
                    student.password = make_password(new_password)
                    student.save()
                    messages.success(request, 'Password changed successfully!')
                else:
                    messages.error(request, 'New password and confirm password do not match!')
            else:
                messages.error(request, 'Old password is incorrect!')
    
    try:
        cse_instance = Computer_Science_and_Engineering.objects.get(student_ID=student_ID)
        name = cse_instance.name
        email = cse_instance.email
        phone = cse_instance.phone
    except Computer_Science_and_Engineering.DoesNotExist:
        ise_instance = Information_Science_and_Engineering.objects.get(student_ID=student_ID)
        name = ise_instance.name
        email = ise_instance.email
        phone = ise_instance.phone

    context = {
        'current_date': current_date,
        'student_ID': student_ID,
        'name': name,
        'email': email,
        'phone': phone,
    }
    return render(request, 'studentportal/student_settings.html', context)


# API that will return pending payment details of a student to a frontend.
def pending_fees(request):

    # Exmaple -> STCSE001 is a current logged_in_student.
    Current_student_logged_in = request.session['ID']
    payment_details_table = ''

    # Branch data -> course details that are available in college.
    Branch_data = list(Course.objects.all().values())

    # Student Id is reduced to CSE as per example
    verification_student = Current_student_logged_in[2:(len(
        Current_student_logged_in)-3)]

    # Identifying to which Branch student belongs. Final it is appended with _fd which is table which holds payment details of student
    for data in Branch_data:
        if verification_student == data['course_ID'][0:(len(data['course_ID'])-2)]:
            payment_details_table = data['course_ID']+'_fd'

    # Converting it to lowercase.
    payment_details_table = payment_details_table.lower()

    # First we will extract payment Id which student has to pay.
    with connection.cursor() as cursor:
        query = f'select Id from {payment_details_table} where {Current_student_logged_in} is null'
        cursor.execute(query)
        # data format of Fees_Id [(1,) (2,), (3,)]
        id_list = cursor.fetchall()

        complete_data = []

        # Constructing the payment details that student need to pay.
        for id in id_list:
            db_data = (Fees_details.objects.get(id=id[0]))
            fee_info = {
                'id': db_data.id,
                'description': db_data.description,
                'amount': db_data.amount,
                'start_date': db_data.start_date,
                'end_date': db_data.end_date
            }
            complete_data.append(fee_info)
    return JsonResponse(complete_data, safe=False)


# authorize razorpay client with API Keys which is used to crete order.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# This will send data to the frontend that will help to invoke razerpay API
@csrf_exempt
def razorpay_invoke_data(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('paymentId')

        session_key = request.session.session_key

        Current_student_logged_in = request.session['ID']

        fees_details_taken_from_db = Fees_details.objects.get(id=payment_id)
        fees_details_taken_from_db_amount = fees_details_taken_from_db.amount

        # This is for obtaining branch code of student.
        branch_code_of_a_student = ''  # The course_ID to which student belongs

        Branch_data = list(Course.objects.all().values())
        verification_student = Current_student_logged_in[2:(len(
            Current_student_logged_in)-3)]

        for data in Branch_data:
            if verification_student == data['course_ID'][0:(len(data['course_ID'])-2)]:
                branch_code_of_a_student = data['course_ID']

        # This code is not general, will update in the future.
        student_branch_table = Model_Mapping.get(
            branch_code_of_a_student)  # Table containing student details
        student_data = student_branch_table.objects.get(
            student_ID=Current_student_logged_in)

        # Updation for global variable.
        currency = 'INR'
        # Value of amount is in paisa.
        amount = fees_details_taken_from_db_amount*100
        global amount_student_going_to_pay
        amount_student_going_to_pay = amount  # paisa

        # Creating Razerpay order.
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           # Do not capture it.
                                                           payment_capture='0',
                                                           # Addtional details
                                                           notes={
                                                               'student_ID': student_data.student_ID,
                                                               'student_name': student_data.name,
                                                               'student_email': student_data.email,
                                                               'amount': fees_details_taken_from_db_amount,
                                                               'paymentid': payment_id,
                                                               'session_key': session_key
                                                           }))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://localhost:8000/stu/paymenthandler/'

        # Details to be passed to frontend template.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = str(amount)
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['student_ID'] = student_data.student_ID
        context['student_name'] = student_data.name
        context['student_email'] = student_data.email
        context['session_key'] = session_key

        print(context)

        return JsonResponse(context, safe=False)

 # RazerPay will make post request to this URL.

# This will handle post request made by the razerpay on payment.


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":

        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        }

        print(params_dict)

        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is not None:
            global amount_student_going_to_pay
            amount = amount_student_going_to_pay

            razorpay_client.payment.capture(payment_id, amount)

            payment_details = razorpay_client.payment.fetch(
                payment_id)

            created_at_timestamp = payment_details.get(
                'created_at', 0)

            created_at = make_aware(
                datetime.fromtimestamp(created_at_timestamp))

            formatted_date = created_at.strftime('%d/%m/%y')

            notes = payment_details.get('notes', {})

            student_email = notes.get('student_email')
            student_name = notes.get('student_name')
            student_ID = notes.get('student_ID')
            amount_note = notes.get('amount')
            notes_payment_id = notes.get('paymentid')
            session_key = notes.get('session_key')

            if session_key:
                try:
                    session = Session.objects.get(session_key=session_key)
                    session_data = session.get_decoded()
                    for key, value in session_data.items():
                        request.session[key] = value
                    print("ok")
                except Session.DoesNotExist:
                    print("not ok")

            print(
                "***************************************************************************")
            print(created_at)
            print(formatted_date)
            print(student_ID)
            print(student_name)
            print(student_email)
            print(amount_note)
            print(notes_payment_id)
            print(
                "***************************************************************************")

            # This variable holds to which department the student belogs.
            student_department = str("")

            payment_details_table = ''

            Branch_data = list(Course.objects.all().values())
            verification_student = student_ID[2:(len(
                student_ID)-3)]

            for data in Branch_data:
                if verification_student == data['course_ID'][0:(len(data['course_ID'])-2)]:
                    payment_details_table = data['course_ID']+'_fd'
                    student_department = data['course_name']

            payment_details_table = payment_details_table .lower()

            # Extraxting the fee_receipt ID.

            Fees_ID = int(0)
            with connection.cursor() as cursor:
                cursor.execute(
                    "select *from information_schema.tables where table_schema='payment' and table_name='fee_cnt' limit 1;")
                if cursor.fetchall() == ():
                    cursor.execute("create table fee_cnt (cnt bigint);")
                    cursor.fetchall()
                    cursor.execute("insert into fee_cnt (cnt) values (1);")
                cursor.execute("select cnt from fee_cnt;")
                Fees_ID = cursor.fetchall()[0][0]
                cursor.execute("update fee_cnt set cnt=cnt+1")

            payment_data = str(payment_id)+"//" + \
                formatted_date+"//"+str(amount_note)+"//RCC"+str(Fees_ID)

            with connection.cursor() as cursor:
                query = f"update {payment_details_table } set {student_ID}='{payment_data}' where Id={notes_payment_id};"
                cursor.execute(query)

            # Sending email and automatic pdf receipt generation code.

            send_email(student_email, student_name, student_ID,
                       student_department, formatted_date, (amount_note), "RCC"+str(Fees_ID))

        # return render(request, 'studentportal/student_payment.html', {})

            # request.session['logged_in'] = True
            # # Student_ID is stored in the session.
            # request.session['ID'] = "123456"

            return redirect('/stu/payment/')
        else:
            print("Signature verification failed")
            # return render(request, 'paymentfail.html', {})
            return redirect('/stu/dashboard/')
    else:
        return HttpResponseBadRequest()


# API that will return fees paid by a student to the frontend -> Transaction page of a student.
def student_transaction(request):

    current_student_logged_in = request.session['ID']
    Branch_data = list(Course.objects.all().values())

    verification_student = current_student_logged_in[2:(
        len(current_student_logged_in)-3)]

    for data in Branch_data:
        if verification_student == data['course_ID'][0:(len(data['course_ID'])-2)]:
            course_id = data['course_ID']

    payment_details_table = course_id+'_fd'

    with connection.cursor() as cursor:
        cursor.execute(
            f"select id, {current_student_logged_in} from {payment_details_table} where {current_student_logged_in} is not null")

        id_list = cursor.fetchall()

        data = []
        for id in id_list:
            row = Fees_details.objects.get(id=id[0])
            split = id[1].split('//')
            payment_info = {

                'transaction_id': split[0],
                'amount': split[2],
                'date': split[1],
                'description': row.description,
            }
            data.append(payment_info)
    return JsonResponse(data, safe=False)

# Function that will convert number into text.


def convert_to_words(num):

    num = int(num)

    if num == 0:
        return "zero"
    ones = ["", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine"]
    tens = ["", "", "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen",
             "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    words = ""

    # This will handle value from  0 to 9, 99, 999

    # 1 to 9 lakh
    if num >= 100000:
        words += ones[num // 100000] + " lakh "
        num %= 100000

    # 1 thousand to 99 thousand
    if num >= 1000:
        cnt = num // 1000
        if cnt >= 10:
            if cnt >= 10 and cnt <= 19:
                words += teens[cnt - 10] + " thousand "
            else:
                words += tens[cnt // 10] + " "
                cnt %= 10
                if cnt >= 1 and cnt <= 9:
                    words += ones[cnt] + " "
                words += "thousand "
        else:
            words += ones[num // 1000] + " thousand "
        num %= 1000  # This should happen in all cases.

    # 100 to 999
    if num >= 100:
        words += ones[num // 100] + " hundred "
        num %= 100

    # handels less then 20 values.
    if num >= 20:
        words += tens[num // 10] + " "
        num %= 10
        if num >= 1 and num <= 9:
            words += ones[num] + " "

    elif num >= 10 and num <= 19:
        words += teens[num - 10] + " "
        num = 0

    else:
        words += ones[num] + " "

    return words.strip()


# Function that will create a pdf
def Create_pdf(Sname, Sid, Sbranch, Sdate, Samount, receipt_no):

    filename = 'Receipt.pdf'
    documentTitle = 'Receipt'
    custom_size = (400, 600)

    pdf = canvas.Canvas(filename, pagesize=custom_size)
    pdf.setTitle(documentTitle)
    pdfmetrics.registerFont(TTFont('abc', 'Receipt\SakBunderan.ttf'))

    # Border set up.
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor(colors.white)
    pdf.rect(20, 20, 360, 560)

    # Line has been drawn.
    pdf.line(20, 480, 380, 480)
    pdf.line(20, 450, 380, 450)
    pdf.line(20, 330, 380, 330)
    pdf.line(20, 300, 380, 300)
    pdf.line(20, 100, 380, 100)

    # Cross Lines.
    pdf.line(60, 100, 60, 330)
    pdf.line(300, 100, 300, 330)

    image1 = 'Receipt\Logo.jpeg'

    image2 = 'Receipt\Sign.jpeg'

    pdf.drawInlineImage(image1, 25, 495, 60, 80)
    pdf.drawInlineImage(image2, 280, 30, 30, 30)

    address_line1 = "123 Learning Lane"
    address_line2 = "Knowledge City, IN 45678"
    address_line3 = "Phone: (555) 123-4567"

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawCentredString(200, 555, 'VISHWA COACHING CENTER')
    pdf.setFont('Helvetica', 12)
    pdf.drawString(95, 535, address_line1)
    pdf.drawString(95, 515, address_line2)
    pdf.drawString(95, 495, address_line3)

    # Basic Student Details.
    Name = str(Sname)
    Id = str(Sid)
    Branch = str(Sbranch)
    Date = str(Sdate)
    Receipt = str(receipt_no)

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('Courier-Bold', 14)

    pdf.drawString(21, 430, 'RECEIPT NO: '+Receipt)
    pdf.drawString(21, 406, 'NAME: '+Name)
    pdf.drawString(21, 384, 'ID: '+Id)
    pdf.drawString(21, 362, 'BRANCH: '+Branch)
    pdf.drawString(21, 340, 'DATE: '+Date)

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('Courier-Bold', 16)
    pdf.drawCentredString(180, 465, 'RECEIPT')

    pdf.setFont('Courier-Bold', 14)
    pdf.drawCentredString(40, 315, 'Sl')
    pdf.drawCentredString(180, 315, 'Particulars')
    pdf.drawCentredString(340, 315, 'Amount')

    particulars = 'Examination Fees'
    amount = str(Samount)

    pdf.setFont('Courier-Bold', 12)
    pdf.drawCentredString(40, 280, '1')
    pdf.drawString(65, 280, particulars)
    pdf.drawCentredString(340, 280, amount)

    pdf.setFont('Courier-Bold', 14)
    pdf.drawCentredString(270, 120, 'TOTAL')

    total = str(Samount)
    pdf.setFont('Courier-Bold', 12)
    pdf.drawCentredString(340, 120, total)

    InWords = convert_to_words(int(total)) + ' only'
    pdf.setFont('Courier-Bold', 12)
    pdf.drawString(20, 80, 'In Words: ')

    words = InWords.split()  # String is breked into words
    chunks = [' '.join(words[i:i + 6]) for i in range(0, len(words), 6)]

    line_space = int(80)
    line_start = 85

    for chunk in chunks:
        pdf.drawString(line_start, line_space, chunk)
        line_space -= 15
        line_start = 20

    # pdf.drawString(85, 80, InWords)

    pdf.drawString(225, 22, 'Authorized Signature')

    pdf.save()


# Function that will send mail to the student.

def send_email(email_id, name, id, branch, date, amount, receipt_no):

    subject = 'Fee Receipt'
    message = 'Please find the attached fee receipt'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email_id]

    Create_pdf(name, id, branch, date, int(amount), receipt_no)
    # Prepared Receipt folder path.
    # pdf_path = os.path.join(settings.BASE_DIR, './Receipt/Receipt.pdf')
    pdf_path = os.path.join(settings.BASE_DIR, './Receipt.pdf')
    print(pdf_path)
    print(settings.BASE_DIR)

    email = EmailMessage(subject, message, from_email, recipient_list)

    # Opening a file and reading the content of the file.
    # Receipt.pdf is name of pdf formed in the client side by browser
    # f.read() -> reading the content of the file.
    # 'application/pdf' -> indicating it is PDF content.
    with open(pdf_path, 'rb') as f:
        email.attach('Receipt.pdf', f.read(), 'application/pdf')

    email.send()  # Sending the Email.


# Updating API transaction
# configring add button
# updating email sending and pdf generation.
# Report display
# configruing middleware.


def demo(request):
    return JsonResponse("GOOD", safe=False)
