# Generated by Django 4.0.4 on 2022-05-17 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0006_alter_useremail_options_useremail_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useremail',
            options={'ordering': ('order',)},
        ),
    ]
