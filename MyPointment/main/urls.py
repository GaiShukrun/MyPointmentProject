
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
<<<<<<< HEAD
    # path('UserProfile/', views.profile, name='profile'),
    
=======
    path('UserProfile/', views.profile, name='profile'),
    path('ViewAvg/',views.avg_Doctors,name = "ViewAvg"), 
>>>>>>> 7e8f99f42a2687c5a1487553c9cfd918c516c376
]