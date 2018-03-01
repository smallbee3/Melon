from django.urls import path

from . import views

app_name = 'emails'
urlpatterns = [
    path('send/', views.send_email, name='send-email')
]