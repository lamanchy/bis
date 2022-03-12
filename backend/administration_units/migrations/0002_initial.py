# Generated by Django 4.0.3 on 2022-03-11 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration_units', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='administrativeunit',
            name='board_members',
            field=models.ManyToManyField(related_name='administrative_units', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrativeunit',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_units', to='administration_units.administrativeunit'),
        ),
    ]