# Generated by Django 4.1 on 2022-10-31 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_offer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='offer'),
        ),
    ]
