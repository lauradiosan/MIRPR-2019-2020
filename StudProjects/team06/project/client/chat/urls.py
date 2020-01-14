from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('send_text', views.send_text, name='send_text'),
]
