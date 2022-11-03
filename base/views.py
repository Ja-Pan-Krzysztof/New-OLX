from .models import Tags, Offer, Location, Category

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from .forms import OfferForm


def home(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        template_name = 'base/offers.html'
        pattern = request.POST['pattern']

        offers = Offer.objects.filter(
            Q(topic__icontains=pattern) |
            Q(tags__tag__icontains=pattern) |
            Q(category__name__icontains=pattern) |
            Q(description__icontains=pattern) |
            Q(host__username__icontains=pattern)
        )

        context = {
            'categories': categories,
            'offers': offers
        }

        return render(request, template_name, context)

    if request.method == 'GET':
        template_name = 'base/home.html'

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

        #tags = request.POST['tags']
        category = request.POST['category']
        topic = request.POST['topic']
        #location = request.POST['location']

        #try:
        #    Tags.objects.get(id=tags)

        #except:
        #    return JsonResponse({'addoffer': 2})

        try:
            Category.objects.get(id=category)

        except:
            return JsonResponse({'addoffer': 3})

        #try:
        #    Location.objects.get(id=location)

        #except:
        #    return JsonResponse({'addoffer': 5})

        if len(topic) > 50:
            return JsonResponse({'addoffer': 4})

        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.host = request.user
            new_offer.save()

            return redirect('home')

        return JsonResponse({'addoffer': 1})

    if request.method == 'GET':
        form = OfferForm()

        context = {
            'form': form,
        }

        return render(request, template_name, context)


def offer_category(request, category_name=None):
    template_name = 'base/offer-category.html'

    context = {}
    if category_name is None:
        categories = Category.objects.all()
        context['categories'] = categories
        context['category_bool'] = True

    if category_name is not None:
        categories = Offer.objects.filter(category__name=category_name)
        context['offers'] = categories

    return render(request, template_name, context)
