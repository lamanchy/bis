# Generated by Django 3.2.15 on 2022-09-20 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_auto_20220920_0754'),
        ('event', '0021_auto_20220920_0754'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventApplication',
        ),
        migrations.DeleteModel(
            name='EventApplicationAddress',
        ),
        migrations.DeleteModel(
            name='EventApplicationClosePerson',
        ),
    ]