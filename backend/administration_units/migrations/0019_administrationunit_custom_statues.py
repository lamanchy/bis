# Generated by Django 3.2.15 on 2022-10-23 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration_units', '0018_auto_20220811_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrationunit',
            name='custom_statues',
            field=models.FileField(blank=True, upload_to='custom_statues'),
        ),
    ]
