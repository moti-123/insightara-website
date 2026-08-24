from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "company", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com"}),
            "company": forms.TextInput(attrs={"placeholder": "Company (optional)"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us about your project...", "rows": 5}),
        }
