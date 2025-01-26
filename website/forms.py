from django import forms
from django.contrib.auth.models import User
from .models import Profile  # Assuming Profile model is being used for additional fields

class SignUpForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('business_owner', 'Business Owner'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select, label="Register as")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
