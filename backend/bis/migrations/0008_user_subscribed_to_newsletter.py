# Generated by Django 3.2.16 on 2023-01-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0007_remove_event_is_internal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribed_to_newsletter',
            field=models.BooleanField(default=True),
        ),
    ]