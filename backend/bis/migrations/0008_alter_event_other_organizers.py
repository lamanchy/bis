# Generated by Django 4.0.4 on 2022-05-17 12:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0007_alter_useremail_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='other_organizers',
            field=models.ManyToManyField(blank=True, related_name='events_where_was_organizer', to=settings.AUTH_USER_MODEL),
        ),
    ]
