from django import forms
from .models import Application, Document


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['gpa', 'school_name', 'year_level', 'course', 'essay']
        widgets = {
            'essay': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your personal statement here...'}),
            'gpa': forms.NumberInput(attrs={'step': '0.01', 'min': '1.0', 'max': '4.0'}),
        }
        labels = {
            'gpa': 'GPA / Grade Average',
            'school_name': 'School / University',
            'year_level': 'Year Level',
            'course': 'Program / Course',
            'essay': 'Personal Statement / Essay',
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'file_type']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
            if hasattr(file, 'content_type') and file.content_type not in allowed_types:
                raise forms.ValidationError("Only PDF, JPEG, and PNG files are allowed.")
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File must be under 10MB.")
        return file


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'review_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'review_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
