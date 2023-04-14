from django.urls import path
from .views import *

urlpatterns = [
    path('', faceRecognition, name='face recognition'),
]
