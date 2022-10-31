from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Offer


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['topic', 'category', 'description', 'image', 'price']



