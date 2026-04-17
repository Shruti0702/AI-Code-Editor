from django.db import models
from django.contrib.auth.models import User

class SavedSnippet(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title