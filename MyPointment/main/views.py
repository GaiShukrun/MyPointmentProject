from django.shortcuts import render, redirect
from urllib import request
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,get_user_model
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from main.forms import SignUpForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from booking.models import Appointment

# def Base(response):
#     return render(response , 'Base.html',{})
def home(response):
    return render(response , 'HomePage.html',{})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if (username == "Cardiologist" or username == "Oncologist" or username == "Psychiatrist" or username == "Neurologist"):
                    login(request,user)
                    return redirect("CardiologistApp")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
           
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def register_user(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
          user = form.save()
        #   username = form.cleaned_data.get('username')
        #   password = form.cleaned_data.get('password')
        #   user = authenticate(username = username , password = password )
          login(request,user)
          messages.success(request,("registration successful"))
          return redirect('home')
       
        messages.error(request,("registration error"))
            
    
    form=SignUpForm()
    return render (request=request, template_name="register.html", context={"register_form":form})
 

def logout_user(request):
    logout(request)
    return redirect('home')

# def BhiratTor(response):
#     return render(response , 'BhiratTor.html',{})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='password_reset.html', context={"password_reset_form":password_reset_form})

# def profile(response):
#     return render(response , 'UserProfile.html',{})

def avg_Doctors(request):
    mydata = Appointment.objects.all()
    count1,count2,avg = 0,0,0
    countCar,countCar2,avgCar = 0,0,0
    countOnco,countOnco2,avgOnco =0,0,0
    countPsy,countPsy2,avgPsy =0,0,0
    countNeu,countNeu2,avgNeu = 0,0,0
    
    for obj in mydata:
        count1+=1
        if obj.Apperence == True :
            count2+=1
            if obj.timetaken != None:
                avg += int(obj.timetaken)
        if  obj.service == 'Cardiologist' :
            countCar+=1
            if obj.Apperence == True :
                countCar2+=1
                if obj.timetaken != None:
                    avgCar += int(obj.timetaken)
                
        if  obj.service == 'Oncologist' :
            countOnco+=1
            if obj.Apperence == True  :
                countOnco2+=1
                if obj.timetaken != None:
                    avgOnco += int(obj.timetaken)
        if  obj.service == 'Psychiatrist' :
            countPsy+=1
            if obj.Apperence == True  :
               countPsy2+=1
               if obj.timetaken != None:
                  avgPsy += int(obj.timetaken)
        if  obj.service == 'Neurologist' :
            countNeu+=1
            if obj.Apperence == True  :
                countNeu2+=1
                if obj.timetaken != None:
                    avgNeu += int(obj.timetaken)
    if count2!=0 :
        # and countCar2!=0 and countPsy!= 0 and countNeu2!=0:
        avg = avg/count2
    else:
        avg = 0
    if countCar2!=0:
        avgCar = avgCar/countCar2
    else:
        avgCar = 0
    if countOnco2!= 0:
        avgOnco = avgOnco/countOnco2
    else:
        avgOnco = 0
    if countPsy2!= 0:
        avgPsy = avgPsy/countPsy2
    else:
        avgPsy = 0
    if countNeu2 != 0:
        avgNeu = avgNeu/countNeu2
    else:
        avgNeu = 0
    allavg = (avg,avgCar,avgOnco,avgPsy,avgNeu)
    allnumapp = (count1,countCar,countOnco,countPsy,countNeu)
    allnumArrivedapp = (count2,countCar2,countOnco2,countPsy2,countNeu2)


    context = {
        "avg":allavg,
        "NumberOfAppointment":allnumapp,
        "NumberofAppointmentArrived":allnumArrivedapp,
        "App":mydata,
    }

    return render(request,"ViewAvg.html",context)
