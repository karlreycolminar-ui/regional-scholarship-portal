from django import forms
from .models import Scholarship


class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['title', 'description', 'eligibility_criteria',
                  'amount', 'slots', 'category', 'deadline', 'is_active']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'eligibility_criteria': forms.Textarea(attrs={'rows': 4}),
        }
