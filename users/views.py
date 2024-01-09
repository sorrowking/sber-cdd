from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .forms import RegistrationForm, LoginForm
from .models import Profile
import datetime

class RegistrationError(Exception):
    pass


def check_password_difficulty(password):
    if len(password) <= 8:
        return 'В пароле должно быть хотя бы 9 символов'
    is_up = False
    is_down = False
    has_dig = False
    for i in range(len(password)):
        if password[i].isupper():
            is_up = True
        elif password[i].islower():
            is_down = True
        if password[i].isdigit():
            has_dig = True
    if not is_up or not is_down:
        return 'В пароле должна быть хотя бы одна заглавная и одна строчная буква'
    if not has_dig:
        return 'В пароле должна быть хотя бы одна цифра'
    return 'ok'

def check_registration_form(form):
    email, password, password_confirmation = form.cleaned_data['email'], form.cleaned_data['password'], form.cleaned_data['password_confirmation']
    if password != password_confirmation:
        raise RegistrationError("Пароли не совпадают")
    status = check_password_difficulty(password)
    if status != 'ok':
        raise RegistrationError(status)
    if (Profile.objects.filter(email=email).count() > 0):
        raise RegistrationError("Почтовый адрес занят")
    return True


def user_login(request):
    form = LoginForm(request.POST)
    user = authenticate(username=form.data['email'], password=form.data['password'])
    if user is not None:
        login(request, user)
        return {"login_error": "", "registration_error": ""}
    return {"login_error": "Неверный логин или пароль", "registration_error": ""}


def user_registration(request):
    errors = {"login_error": "", "registration_error": ""}
    if not request.POST.get('name'):
        return user_login(request)
    form = RegistrationForm(request.POST)
    if form.is_valid():
        try:
            check_registration_form(form)
            user = User.objects.create_user(username=form.cleaned_data['email'],
                                 email=form.cleaned_data['email'],
                                 password=form.cleaned_data['password'])
            form.save()
            user.save()
        except RegistrationError as RegErr:
            errors["registration_error"] = RegErr
    else:
        errors["registration_error"] = "Дата должна быть в формате YYYY-MM-DD"
    return errors