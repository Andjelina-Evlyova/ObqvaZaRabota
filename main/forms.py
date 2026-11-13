from django import forms

from .models import JobApplication, JobPosting


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = (
            "title",
            "company_name",
            "location",
            "work_mode",
            "salary",
            "description",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Напр. Python Developer"}),
            "company_name": forms.TextInput(attrs={"placeholder": "Име на компанията"}),
            "location": forms.TextInput(attrs={"placeholder": "Напр. София"}),
            "salary": forms.TextInput(attrs={"placeholder": "Напр. 1500–2500 € нето"}),
            "description": forms.Textarea(attrs={"placeholder": "Опишете позицията, изискванията и предлаганите условия.", "rows": 7}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("full_name", "email", "profile_url", "message")
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Напр. Мария Иванова", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com", "autocomplete": "email"}),
            "profile_url": forms.URLInput(attrs={"placeholder": "https://linkedin.com/in/..."}),
            "message": forms.Textarea(attrs={"placeholder": "Защо тази позиция е точно за теб?", "rows": 4}),
        }
