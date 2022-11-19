from .models import Tags, Offer, Location, Category

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic as gc
from django.http import JsonResponse
from django.db.models import Q

from .forms import OfferForm

# exceptions
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    template_name = 'base/home.html'
    categories = Category.objects.all()

    if request.method == 'POST':
        pattern = request.POST['pattern']

        offers = Offer.objects.filter(
            Q(topic__icontains=pattern) |
            Q(description__icontains=pattern) |
            Q(category__name__icontains=pattern) |
            Q(host__username__icontains=pattern)
        )

        context = {
            'categories': categories,
            'offers': offers,
        }

        return render(request, template_name='base/offers.html', context=context)

    if request.method == 'GET':
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
        # tags = request.POST['tags']
        category = request.POST['category']
        topic = request.POST['topic']
        # location = request.POST['location']

        # try:
        #    Tags.objects.get(id=tags)

        # except:
        #    return JsonResponse({'addoffer': 2})

        try:
            Category.objects.get(id=category)

        except:
            return JsonResponse({'addoffer': 'Bad Category'})

        # try:
        #    Location.objects.get(id=location)

        # except:
        #    return JsonResponse({'addoffer': 5})

        if len(topic) > 50:
            return JsonResponse({'addoffer': 'Topic is too long.'})

        try:
            offer = Offer(
                host=request.user,
                topic=topic,
                category=Category.objects.get(id=4),
                description=request.POST['description'],
                image=request.FILES['image'],
                price=request.POST['price']
            )
            offer.save()

        except MultiValueDictKeyError:
            offer = Offer(
                host=request.user,
                topic=topic,
                category=Category.objects.get(id=4),
                description=request.POST['description'],
                image=None,
                price=request.POST['price']
            )
            offer.save()

        finally:
            return JsonResponse({'addoffer': 0})

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
        if category_name == 'All':
            categories = Offer.objects.all()

        else:
            categories = Offer.objects.filter(category__name=category_name)

        context['offers'] = categories

    return render(request, template_name, context)


class OfferId(gc.DetailView):
    template_name = 'base/offer.html'
    model = Offer

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['offer'] = Offer.objects.get(id=self.object.id)

        return context






