from django.urls import path
from .views import explain_error

urlpatterns = [
    path('explain-error/', explain_error, name='explain_error'),
]