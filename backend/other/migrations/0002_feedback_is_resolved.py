# Generated by Django 3.2.16 on 2023-01-29 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_resolved',
            field=models.BooleanField(default=False),
        ),
    ]
