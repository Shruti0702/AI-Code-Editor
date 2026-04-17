from django.urls import path
from .views import editor_page, run_code, save_snippet, snippet_list

urlpatterns = [
    path('', editor_page, name='editor'),
    path('run/', run_code, name='run_code'),
    path('save/', save_snippet, name='save_snippet'),
    path('snippets/', snippet_list, name='snippet_list'),
]