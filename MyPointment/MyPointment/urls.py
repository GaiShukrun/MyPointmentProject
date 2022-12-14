
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('',include('booking.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),      
    path('UserProfile/change-password/',
        auth_views.PasswordChangeView.as_view(template_name='change-password.html', success_url = '/' ),name='change_password'),
    path('',include('Doctors.urls')),
    
]
