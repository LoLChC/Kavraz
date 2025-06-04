from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basit doğrulamalar
        if password1 != password2:
            messages.error(request, 'Şifreler uyuşmuyor.')
            return render(request, 'account/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
            return render(request, 'account/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kayıtlı.')
            return render(request, 'account/register.html')

        # Kullanıcı oluştur
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
        )

        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('/account/login')  # Giriş sayfanın URL'si

    return render(request, 'account/register.html') 

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('/')  # Girişten sonra yönlendirme
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')

    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('/account/login')


def account(request):
    return render(request, 'account/account.html')
