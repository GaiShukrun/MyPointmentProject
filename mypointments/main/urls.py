from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("dafmetupal/", views.dafmetupal, name="DafMetupal"),
    path('login/', views.login_view, name='login'),
    path('dafadmin',views.dafadmin, name='DafAdmin'),
    path('signout/', LogoutView.as_view(), name='signout'),
]

urlpatterns += {}