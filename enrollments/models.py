from django.db import models
from clients.models import Client
from programs.models import Program
from accounts.models import User
import uuid
from django.utils import timezone


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped Out'),
        ('PAUSED', 'Paused')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    enrolled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [('client', 'program')]
        ordering = ['-enrollment_date']

    def save(self, *args, **kwargs):
        if self.status == 'COMPLETED' and not self.completed_date:
            self.completed_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} in {self.program} ({self.status})"