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

def Base(response):
    return render(response , 'Base.html',{})
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
          messages.success(request,("registretion successful"))
          return redirect('home')
       
        messages.error(request,("registeration errror"))
            
    
    form=SignUpForm()
    return render (request=request, template_name="register.html", context={"register_form":form})
 

def logout_user(request):
    logout(request)
    return redirect('home')

def BhiratTor(response):
    return render(response , 'BhiratTor.html',{})

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

def profile(response):
    return render(response , 'UserProfile.html',{})
