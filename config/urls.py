from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/editor/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('editor/', include('editor.urls')),
    path('problems/', include('problems.urls')),
    path('submissions/', include('submissions.urls')),
    path('ai/', include('ai_assistant.urls')),
]