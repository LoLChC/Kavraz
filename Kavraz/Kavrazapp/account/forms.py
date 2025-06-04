# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Eğer özelleştirmediysen

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # veya CustomUser kullanıyorsan onu yaz
        fields = ['username', 'email', 'password1', 'password2']
