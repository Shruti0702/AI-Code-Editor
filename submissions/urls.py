from django.urls import path
from .views import submission_list

urlpatterns = [
    path('', submission_list, name='submission_list'),
]