# Generated by Django 4.1 on 2022-10-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
