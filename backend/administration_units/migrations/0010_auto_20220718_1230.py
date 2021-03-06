# Generated by Django 3.2.14 on 2022-07-18 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0009_zipcode'),
        ('administration_units', '0009_administrationunitcontactaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrationunitaddress',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='other.region'),
        ),
        migrations.AddField(
            model_name='administrationunitcontactaddress',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='other.region'),
        ),
    ]
