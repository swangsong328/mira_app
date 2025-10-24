"""Custom allauth adapter for username-less authentication."""
from __future__ import annotations

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for email-only authentication.
    
    Removes username field requirements since Customer model doesn't have username.
    """
    
    def is_open_for_signup(self, request):
        """
        Check if signups are allowed.
        """
        return super().is_open_for_signup(request)
    
    def populate_username(self, request, user):
        """
        Auto-generate username from email.
        Username field exists but is not used for authentication.
        """
        if user.email and not user.username:
            # Generate username from email (before @ symbol)
            import uuid
            base_username = user.email.split('@')[0]
            # Add unique suffix to ensure uniqueness
            user.username = f"{base_username}_{uuid.uuid4().hex[:8]}"
    
    def clean_username(self, username, shallow=False):
        """
        Username validation - auto-generate if not provided.
        """
        # Username is auto-generated from email, no need to validate
        return username or ""
    
    def save_user(self, request, user, form, commit=True):
        """
        Save the user with email (no username).
        """
        # Get email from form
        email = form.cleaned_data.get("email")
        if email:
            user.email = email
        
        # Save if commit requested
        if commit:
            user.save()
        
        return user

