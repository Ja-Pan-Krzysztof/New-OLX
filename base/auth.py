from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model, decorators
from django.http import JsonResponse

from .forms import SingUpUserForm
from .models import AboutUser

import re

# Exceptions

from django.core.exceptions import ObjectDoesNotExist


def email_re(email):
    return True if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email) else False


def username_re(username):
    return True if re.fullmatch(re.compile('^[a-zA-Z0-9_.-]+$'), username) else False


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)

        except ObjectDoesNotExist:
            return JsonResponse({'login': 'Username does not exist.'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return JsonResponse({'login': 0})

        else:
            return JsonResponse({'login': 'Invalid username or password.'})

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

        template_name = 'base/auth/login.html'

        context = {

        }

        return render(request, template_name, context)


def logout_page(request):
    logout(request)

    return JsonResponse({'logout': 0})


def sigh_up_page(request):
    template_name = 'base/auth/sign_up.html'

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if len(username) < 1:
            return JsonResponse({'signup': 'Username is too short.'})

        if not username_re(username):
            return JsonResponse({'signup': 'Invalid username.'})

        if not email_re(email):
            return JsonResponse({'signup': 'Invalid email.'})

        if len(pass1) < 8:
            return JsonResponse({'signup': 'Password is too short.'})

        if not pass1 == pass2:
            return JsonResponse({'signup': 'Passwords are not same.'})

        try:
            if User.objects.get(username=username) is not None:
                return JsonResponse({'signup': 'Username exist.'})

        except ObjectDoesNotExist:
            pass

        try:
            if User.objects.get(email=email.lower()) is not None:
                return JsonResponse({'signup': 'Email exist.'})

        except ObjectDoesNotExist:
            pass

        user = get_user_model()
        user = user.objects.create_user(username=username, password=pass1, email=email.lower())
        user.is_superuser = False
        user.if_staff = False
        user.save()
        
        login(request, user)

        return JsonResponse({'signup': 0})

    if request.method == 'GET':
        form = SingUpUserForm()

        context = {
            'form': form,
        }

        return render(request, template_name, context)


@decorators.login_required
def account_settings(request, username=None):
    template_name = 'base/auth/account-settings.html'

    if request.method == 'GET':
        if username is None:
            username = request.user.username

            return redirect('account-settings', username=username)

        if username is not None:
            user = User.objects.get(username=username)
            context = {
                'user_settings': user
            }
            try:
                about_user = AboutUser.objects.get(user=user)
                context['about_user'] = about_user

            except ObjectDoesNotExist:
                pass

            return render(request, template_name, context)

    if request.method == 'POST':
        s_u = request.POST['username']
        s_e = request.POST['email']
        s_f = request.POST['firstname']
        s_ln = request.POST['lastname']
        s_p = request.POST['publicemail']
        s_b = request.POST['bio']
        s_c = request.POST['company']
        s_l = request.POST['location']

        user = User.objects.get(id=request.POST['id_user'])

        if not email_re(s_e):
            return JsonResponse({'updateProfile': 1})

        if s_p != '':
            if not email_re(s_p):
                return JsonResponse({'updateProfile': 2})

        if s_u != user.username:
            try:
                User.objects.get(username=s_u)

                return JsonResponse({'updateProfile': 3})

            except ObjectDoesNotExist:
                pass

        if s_e != user.email:
            try:
                User.objects.get(email=s_e)

                return JsonResponse({'updateProfile': 4})

            except ObjectDoesNotExist:
                pass

        else:
            s_e = user.email

        try:
            AboutUser.objects.get(user=user)
            AboutUser.objects.filter(user=user.id)\
                .update(firstname=s_f, lastname=s_ln, public_email=s_p, bio=s_b, company=s_c, location=s_l)

        except ObjectDoesNotExist:
            about_user = AboutUser.objects\
                .create(user=user, firstname=s_f, lastname=s_ln, public_email=s_p, bio=s_b, company=s_c, location=s_l)
            about_user.save()

        user = User.objects.filter(id=request.POST['id_user'])
        user.update(username=s_u, email=s_e)

        return JsonResponse({'updateProfile': 0, 'redirect': s_u})
