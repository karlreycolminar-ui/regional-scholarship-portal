from django.db import models
from django.conf import settings


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='applications'
    )
    scholarship = models.ForeignKey(
        'scholarships.Scholarship', on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Personal / academic info
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    school_name = models.CharField(max_length=255, blank=True)
    year_level = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=255, blank=True)
    essay = models.TextField(blank=True, help_text='Personal statement / essay')

    # Review info
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    date_submitted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_submitted']
        unique_together = ['user', 'scholarship']  # one application per scholarship

    def __str__(self):
        return f"{self.user.username} → {self.scholarship.title} ({self.status})"


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('transcript', 'Transcript of Records'),
        ('id', 'Government ID'),
        ('recommendation', 'Recommendation Letter'),
        ('income', 'Income Certificate'),
        ('birth_cert', 'Birth Certificate'),
        ('other', 'Other'),
    ]

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='documents'
    )
    file = models.FileField(upload_to='documents/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.application}"

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = self.file.name
        super().save(*args, **kwargs)
