from django.db import models
from django.utils import timezone


class Scholarship(models.Model):
    CATEGORY_CHOICES = [
        ('merit', 'Merit-Based'),
        ('need', 'Need-Based'),
        ('sports', 'Sports'),
        ('arts', 'Arts & Culture'),
        ('stem', 'STEM'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slots = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        related_name='created_scholarships'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Scholarships'

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        return self.is_active and self.deadline > timezone.now()

    @property
    def days_remaining(self):
        delta = self.deadline - timezone.now()
        return max(0, delta.days)
