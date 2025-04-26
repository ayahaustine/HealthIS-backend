from . utils import CustomIDField
from django.conf import settings
from django.db import models
import uuid

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    uuid = CustomIDField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients'
    )

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
