from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """Model representing a doctor record."""

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctors',
        help_text="The user who created this doctor record.",
    )
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
