# Generated by Django 4.0.4 on 2022-05-17 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-start',)},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',)},
        ),
    ]
