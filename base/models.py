from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    voivodeship = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.voivodeship


class Tags(models.Model):
    tag = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag


class Offer(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=50, null=False)
    tags = models.ManyToManyField(Tags, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='offer/')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    particopants = models.ManyToManyField(User, related_name='particopants', blank=True)
    views = models.IntegerField(null=False, default=0)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic[:50]

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
















