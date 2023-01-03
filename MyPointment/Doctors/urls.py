from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from .views import generatePDF

urlpatterns = [ 
    path('CardiologistApp/',views.ViewAppointment,name="CardiologistApp"),
    path('CardiologistApp/pdf/',views.generatePDF),
    path('DeleteApp/<int:id>',views.DeleteApp,name = "DeleteApp"),
    path('UpdateTime/<int:id>',views.UpdateTime,name ="UpdateTime"),
   

]