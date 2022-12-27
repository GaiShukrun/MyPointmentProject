from django.shortcuts import render
from booking.models import Appointment
from django.template import loader
from django.http import HttpResponse,FileResponse
import reportlab
from reportlab.pdfgen import canvas
import io 
from fpdf import  FPDF
from django.contrib.auth.models import User

def ViewAppointment(request):
    mydata = Appointment.objects.all()
    user1 = request.user.username
    
        
    return render(request,"CardiologistApp.html",{'App' : mydata,'name':user1} )
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

    