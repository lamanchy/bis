# Generated by Django 4.0.5 on 2022-06-13 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0015_location_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='area',
        ),
    ]
