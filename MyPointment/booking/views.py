from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse,FileResponse
from fpdf import  FPDF


# Create your views here.

def index(request):
    return render(request, "HomePage.html",{})

def booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
        })

def bookingSubmit(request):
    user = request.user
    workdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday"]
    times = [
        "7:30 AM","8:00 AM","8:30 AM","9:00 AM","9:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM","12:00 PM","12:30 PM",
        "1:00 PM","1:30 PM","2:00 PM","2:30 PM","3:00 PM",
        "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM"
    ]
    tomorrow = datetime.now() + timedelta(1)
    minDate = tomorrow.strftime('%Y-%m-%d')
    deltatime = tomorrow + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    
    
    
   
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)
        syptoms = request.POST.get("freeform")
        

        if service != None:
            if day <= maxDate and day >= minDate:
                if date in workdays:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                                syptoms = syptoms,

                            )
                            
                            
                            
                            messages.success(request, "Appointment Saved!")
                            subject = "Password Reset Requested"
                            email_template_name = "Appointment_sent.txt"
                            c = {
                            "email":user.email,
                            'domain':'127.0.0.1:8000',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            "service":service,
                            "day":day,
                            "time":time,

                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                            email = render_to_string(email_template_name, c)
                            try:
                                send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                            except BadHeaderError:
                                return HttpResponse('Invalid header found.')
                            return redirect('/')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")


    return render(request, 'bookingSubmit.html', {
        'times':hour,
    })

def userPanel(request):
    docs = ["Oncologist","Cardiologist","Psychiatrist","Neurologist"]
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
        'docs':docs
    })

def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    tomorrow = datetime.now() + timedelta(1)
    minDate = tomorrow.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (tomorrow + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    workdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday"]
    times = [
        "7:30 AM","8:00 AM","8:30 AM","9:00 AM","9:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM","12:00 PM","12:30 PM",
        "1:00 PM","1:30 PM","2:00 PM","2:30 PM","3:00 PM",
        "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM"
    ]
    tomorrow = datetime.now() + timedelta(1)
    minDate = tomorrow.strftime('%Y-%m-%d')
    deltatime = tomorrow + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date in workdays:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('/')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

# def staffPanel(request):
#     tomorrow = datetime.now() + timedelta(1)
#     minDate = tomorrow.strftime('%Y-%m-%d')
#     deltatime = tomorrow + timedelta(days=21)
#     strdeltatime = deltatime.strftime('%Y-%m-%d')
#     maxDate = strdeltatime
#     #Only show the Appointments 21 days from tomorrow
#     items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

#     return render(request, 'staffPanel.html', {
#         'items':items,
#     })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    workdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday"]
    #Loop days you want in the next 21 days:
    tomorrow = datetime.now() + timedelta(1)
    weekdays = []
    for i in range (0, days):
        x = tomorrow + timedelta(days=i)
        y = x.strftime('%A')
        if y in workdays:
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
    
def DeleteApp1(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return HttpResponseRedirect(reverse('userPanel'))
def generatePDF1(request):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()

    pdf.set_font('courier', 'B', 16)

    pdf.cell(40, 10, 'Your Appointments:',0,1)

    pdf.cell(40, 10, '',0,1)

    pdf.set_font('courier', '', 12)


    pdf.line(10, 30, 150, 30)

    pdf.line(10, 38, 150, 38)

    mydata = Appointment.objects.all().order_by('day','time')
    user1 = request.user

    tmp =''

    for i in mydata:
        if i.service == 'Cardiologist' and i.user == user1  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Oncologist' and i.user == user1  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Psychiatrist' and i.user == user1  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Neurologist' and i.user == user1  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        

    pdf.output('report.pdf', 'F')

    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')