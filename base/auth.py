from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)

        except:
            messages.error(request, 'User doesn\'t exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')

        else:
            messages.error(request, 'Username or password is invalid !')

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

    return redirect('home')


def sigh_up_page(request):
    template_name = 'base/auth/sign_up.html'

    context = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            return redirect('home')

        else:
            messages.error(request, 'Error in form !')

    if request.method == 'GET':
        form = UserCreationForm()

        context = {
            'form': form,
        }

        return render(request, template_name, context)


