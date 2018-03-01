from django.urls import path

from . import views

app_name = 'sms'
urlpatterns = [
    path('send/', views.send_sms, name='sms-send'),
]
