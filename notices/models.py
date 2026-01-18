from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('Exam', 'Exam'),
        ('Event', 'Event'),
        ('Academic', 'Academic'),
        ('Placement', 'Placement'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    # AI-generated summary (bullet points)
    ai_summary = models.TextField(blank=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # PDF notice file
    attachment = models.FileField(upload_to='notices/', null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
 