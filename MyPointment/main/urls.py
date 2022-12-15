
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('',views.Base,name="base"),
    path('', views.home, name="home"),
    path('login/',views.login_user,name="login"),
    path('register/',views.register_user,name="register"),
    path('BhiratTor/',views.BhiratTor,name="BhiratTor"),
    path('logout/',views.logout_user,name="logout"),
    path('password_reset/', views.password_reset_request, name="password_reset"),
    path('UserProfile/', views.profile, name='profile'),
    
]