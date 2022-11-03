from django.test import TestCase
from .models import *
from decimal import Decimal, getcontext

from datetime import datetime as dt

getcontext().prec = 3  # Set precision (two decimal places)


class TestModelsCase(TestCase):
    NOW = dt.now()

    def setUp(self) -> None:
        Category.objects.create(name='Test category')
        Location.objects.create(voivodeship='Test location')

        Offer.objects.create(topic='Test topic',
                             category=Category.objects.get(name='Test category'),
                             description='Test description',
                             image='Test image.png', location=Location.objects.get(voivodeship='Test location'),
                             price=12.4, created=self.NOW, updated=self.NOW
                             )

    def test_verifying_data_correct(self):
        offer = Offer.objects.get(topic='Test topic')
        category = Category.objects.get(name='Test category')
        location = Location.objects.get(voivodeship='Test location')

        self.assertEqual(offer.topic, 'Test topic')
        self.assertEqual(offer.category, Category.objects.get(name='Test category'))
        self.assertEqual(offer.description, 'Test description')
        self.assertEqual(offer.image, 'Test image.png')
        self.assertEqual(offer.location, Location.objects.get(voivodeship='Test location'))
        self.assertEqual(offer.price, Decimal(12.4) / Decimal(1))

        self.assertEqual(category.name, 'Test category')
        self.assertEqual(location.voivodeship, 'Test location')
