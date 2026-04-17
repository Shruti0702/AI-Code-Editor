from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, default='python')
    code = models.TextField()
    stdin = models.TextField(blank=True)
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.created_at}"