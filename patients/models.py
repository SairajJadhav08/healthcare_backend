from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    """Model representing a patient record."""

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patients',
        help_text="The user who created this patient record.",
    )
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_history = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Age: {self.age})"
