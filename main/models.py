from django.db import models

class Request(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    timeAgo = models.CharField(max_length=50, default='Just now')
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    requester_name = models.CharField(max_length=100)
    requester_initials = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
