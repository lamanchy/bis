# Generated by Django 3.2.15 on 2022-09-27 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0048_event_intended_for'),
        ('event', '0024_alter_eventpropagation_intended_for'),
        ('categories', '0012_eventgroupcategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PropagationIntendedForCategory',
            new_name='EventIntendedForCategory',
        ),
    ]
