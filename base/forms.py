from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Offer


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class OfferForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Offer
        fields = ['topic', 'category', 'description', 'image', 'price']


class SingUpUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
