from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from datetime import date


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-posta", required=True)
    phone_number = forms.CharField(label="Telefon Numarası", required=True)
    first_name = forms.CharField(label="Ad", required=True)
    last_name = forms.CharField(label="Soyad", required=True)
    date_of_birth = forms.DateField(
        label="Doğum Tarihi",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email","phone_number", "date_of_birth", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise ValidationError("Kullanıcı adı en az 3 karakter olmalıdır.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu kullanıcı adı zaten alınmış.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Bu telefon numarası zaten kayıtlı.")
        return phone_number

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 13:
            raise ValidationError("13 yaşından küçük kullanıcılar kayıt olamaz.")
        if age > 100:
            raise ValidationError("100 yaşından büyük kullanıcılar kayıt olamaz.")
        return dob
    
    
