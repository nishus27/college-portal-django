# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Grievance(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REPLIED', 'Replied'),
        ('CLOSED', 'Closed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grievances')
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='grievances/', blank=True, null=True)

    reply = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
