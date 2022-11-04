from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse

import re


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)

        except:
            return JsonResponse({'login': 2})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return JsonResponse({'login': 0})

        else:
            messages.error(request, '')

            return JsonResponse({'login': 1})

    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, 'success')
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

        if not pass1 == pass2:
            return JsonResponse({'signup': 2})

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return JsonResponse({'signup': 3})

        if not re.fullmatch(re.compile('^[a-zA-Z0-9_.-]+$'), username):
            return JsonResponse({'signup': 4})

        Userr = get_user_model()
        user = Userr.objects.create_user(username=username, password=pass1, email=email)
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


