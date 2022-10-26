from .models import Tags, Offer, Location, Category

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OfferForm


def home(request):
    template_name = 'base/home.html'

    categories = Category.objects.all()
    offers = Offer.objects.all()

    context = {
        'categories': categories,
        'offers': offers,
    }

    return render(request, template_name, context)


@login_required
def add_offer(request):
    template_name = 'base/add-offer.html'

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)

        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.host = request.user
            new_offer.save()

            return redirect('home')

    if request.method == 'GET':
        form = OfferForm()

        context = {
            'form': form,
        }

        return render(request, template_name, context)
