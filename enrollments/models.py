from django.conf import settings
from django.db import models
import uuid
from clients.models import Client
from programs.models import Program

class Enrollment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enrolled_at']
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'program'],
                name='unique_client_program'
            )
        ]

    def __str__(self):
        return f"{self.client} in {self.program}"
