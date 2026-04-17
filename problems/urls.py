from django.urls import path
from .views import problem_list, problem_detail

urlpatterns = [
    path('', problem_list, name='problem_list'),
    path('<slug:slug>/', problem_detail, name='problem_detail'),
]