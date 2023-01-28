# Generated by Django 3.2.16 on 2023-01-28 21:45

import common.thumbnails
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0009_location_is_fully_specified'),
    ]

    operations = [
        migrations.CreateModel(
            name='EYCACard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', common.thumbnails.ThumbnailImageField(upload_to='eyca_photos')),
                ('number', models.CharField(max_length=63)),
                ('submitted_for_creation', models.BooleanField(default=False)),
                ('sent_to_user', models.BooleanField(default=False)),
                ('valid_till', models.DateField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eyca_card', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
