from . utils import CustomIDField
from django.conf import settings
from django.db import models
import uuid

class Program(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    uuid = CustomIDField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='programs'
    )

    class Meta:
        indexes =  [
            models.Index(fields=['name', 'created_by', 'created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name
