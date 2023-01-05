from django.shortcuts import render,redirect
from booking.models import Appointment
from django.template import loader
from django.http import HttpResponse,FileResponse
import reportlab
from reportlab.pdfgen import canvas
import io 
from fpdf import  FPDF
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F
from .forms import ExampleForm

# Create your views here.


def DeleteApp(request,id):
   
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    
    return HttpResponseRedirect(reverse('CardiologistApp'))
   
   
   
def UpdateTime(request,id):
    if request.method == "POST":
        timetaken = request.POST.get('username')
        appointment = Appointment.objects.get(id=id)
        appointment.timetaken =  timetaken
        if int(timetaken)>0:
            appointment.Apperence = True
            appointment.save()
        else:
            appointment.Apperence = False
            appointment.save()

    return HttpResponseRedirect(reverse('CardiologistApp'))
    

def Send_Email(request):
   
    user = request.user
    subject = "Password Reset Requested"
    email_template_name = "Appointments_sent1.txt"
    mydata = Appointment.objects.all()
    mydata = mydata.order_by('day', 'time')
    user1 = request.user.username
    tmp =''

    for i in mydata:
        if i.service == 'Cardiologist' and user1 == 'Cardiologist'  :
            tmp += str(i)+'\n'
            
        if i.service == 'Oncologist' and user1 == 'Oncologist'  :
            tmp += str(i)+'\n'
            
        if i.service == 'Psychiatrist' and user1 == 'Psychiatrist'  :
            tmp += str(i)+'\n'
            
        if i.service == 'Neurologist' and user1 == 'Neurologist'  :
            tmp += str(i)+'\n'
    c = {
    "email":user.email,
    'domain':'127.0.0.1:8000',
    'site_name': 'Website',
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "user": user,
    "data":tmp,
    'token': default_token_generator.make_token(user),
    'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    #return render(request,"CardiologistApp.html",)
    return HttpResponseRedirect(reverse('CardiologistApp'))
    #return redirect('/CardiologistApp')
    # return render(request,"DoctorApp.html",{'App' : mydata,'name':user1} )
   
def ViewAppointment(request):
    form = ExampleForm()
    mydata = Appointment.objects.all()
    user1 = request.user.username
    template = loader.get_template('CardiologistApp.html')     
    context = {
        'App' : mydata,'name':user1,'form':form
    }  
    return HttpResponse(template.render(context, request)) 
    # return render(request,"CardiologistApp.html",{'App' : mydata,'name':user1} )
# Create your views here.
def generatePDF(request):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()

    pdf.set_font('courier', 'B', 16)

    pdf.cell(40, 10, 'Your Appointments:',0,1)

    pdf.cell(40, 10, '',0,1)

    pdf.set_font('courier', '', 12)


    pdf.line(10, 30, 150, 30)

    pdf.line(10, 38, 150, 38)

    mydata = Appointment.objects.all()
    user1 = request.user.username

    tmp =''

    for i in mydata:
        if i.service == 'Cardiologist' and user1 == 'Cardiologist'  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Oncologist' and user1 == 'Oncologist'  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Psychiatrist' and user1 == 'Psychiatrist'  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        if i.service == 'Neurologist' and user1 == 'Neurologist'  :
            tmp += str(i)
            pdf.cell(200, 8, f"{i}", 0, 1)
        

    pdf.output('report.pdf', 'F')

    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
    
    # return response

    