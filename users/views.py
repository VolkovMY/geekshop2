from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import send_verification_mail
from .models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'title': 'Geekshop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_mail(user)
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)

    context = {
        'title': 'Geekshop - Личный кабинет',
        'form': form,
        'baskets': Basket.objects.filter(user=user),
    }
    return render(request, 'users/profile.html', context)


def verify(request, email, key):
    try:
        user = User.objects.get(email=email, activation_key=key)
        if user.is_activation_key_expired:
            return render(request, "users/verification.html", context={
                'message': "Key is expired"
            })

        user.activate()
        user.save()
        return render(request, "users/verification.html", context={
            'message': "Success"
        })
    except User.DoesNotExist:
        return render(request, "users/verification.html", context={
            'message': "Verification failed"
        })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
