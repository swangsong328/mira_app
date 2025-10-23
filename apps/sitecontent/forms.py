"""Forms for site content."""
from __future__ import annotations

from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Contact form."""

    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "your@email.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+1234567890 (optional)"}),
            "subject": forms.TextInput(attrs={"placeholder": "What's this about?"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Your message...", "rows": 5}
            ),
        }


