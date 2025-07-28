from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Address, UserProfile 
import random
from .forms import RegisterForm
from django.http import JsonResponse
from datetime import datetime, date
from django.contrib.auth import get_user_model
import re

User = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('/account/login')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        UserProfile.objects.create(
            user=user,
            date_of_birth=form.cleaned_data['date_of_birth'],
            phone_number=form.cleaned_data['phone_number'],
        )
        return redirect('/account/login')

    return render(request, 'account/register.html', {
        'form': form,
        'random_number': random.randint(1, 1000),
    })

def validate_register_field(request):
    field = request.GET.get("field")
    value = request.GET.get("value")
    response = {"valid": True, "message": ""}

    if field == "username":
        if len(value) < 3:
            response["valid"] = False
            response["message"] = "Kullanıcı adı en az 3 karakter olmalıdır."
        elif User.objects.filter(username=value).exists():
            response["valid"] = False
            response["message"] = "Bu kullanıcı adı zaten alınmış."
    elif field == "email":
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            response["valid"] = False
            response["message"] = "Geçerli bir e-posta adresi giriniz."

        elif User.objects.filter(email=value).exists():
            response["valid"] = False
            response["message"] = "Bu e-posta adresi zaten kullanılıyor."
    elif field == "phone_number":
        if not re.match(r"^(?:\+90|0090|0)?\s*\(?5\d{2}\)?[\s.-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}$", value):
            response["valid"] = False
            response["message"] = "Geçerli bir telefon numarası giriniz."
            
        elif UserProfile.objects.filter(phone_number=value).exists():
            response["valid"] = False
            response["message"] = "Bu telefon numarası zaten kayıtlı."
    elif field == "date_of_birth":
        try:
            birth_date = datetime.strptime(value, "%Y-%m-%d").date()
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 13:
                response["valid"] = False
                response["message"] = "13 yaşından küçük kullanıcılar kayıt olamaz."
            elif age > 100:
                response["valid"] = False
                response["message"] = "Zaman yolculuğu yapamazsınız, 100 yaşından büyük kullanıcılar kayıt olamaz."
        except:
            response["valid"] = False
            response["message"] = "Geçerli bir tarih giriniz. (YYYY-AA-GG)"

    return JsonResponse(response)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('/')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')

    return render(request, 'account/login.html', {'random_number': random.randint(1, 1000)})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/account/login')

@login_required
def account(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_address':
            Address.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                city=request.POST.get('city'),
                district=request.POST.get('district'),
                address_line=request.POST.get('address_line'),
                is_default=request.POST.get('set_default', False) == 'on'
            )
            return redirect('/account/#address')

        elif form_type == 'edit_address':
            address = get_object_or_404(Address, id=request.POST.get('address_id'), user=request.user)
            address.title = request.POST.get('title')
            address.city = request.POST.get('city')
            address.district = request.POST.get('district')
            address.address_line = request.POST.get('address_line')
            if request.POST.get('set_default') == 'on':
                Address.objects.filter(user=request.user).update(is_default=False)
                address.is_default = True
            address.save()
            return redirect('/account/#address')

        elif form_type == 'delete_address':
            addr = get_object_or_404(Address, id=request.POST.get('address_id'), user=request.user)
            addr.delete()
            return redirect('/account/#address')

        elif form_type == 'set_default':
            Address.objects.filter(user=request.user).update(is_default=False)
            addr = get_object_or_404(Address, id=request.POST.get('address_id'), user=request.user)
            addr.is_default = True
            addr.save()
            return redirect('/account/#address')

        elif form_type == 'change_password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                logout(request)
                return redirect('/account/login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
                request.session['password_modal_open'] = True

    # 🚨 PROFİLİ GETİR VE YOKSA OLUŞTUR
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'date_of_birth': date(2000, 1, 1),  # örnek varsayılan tarih
            'phone_number': '',  # boş telefon numarası
        }
    )

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/account.html', {
        'profile': profile,
        'addresses': addresses,
        'random_number': random.randint(1, 1000),
        'password_modal_open': request.session.pop('password_modal_open', False)
    })


@login_required
def delete_account(request):
    request.user.delete()
    logout(request)
    return redirect('/account/register')
