# Generated by Django 3.2.14 on 2022-07-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration_units', '0008_administrationunit_vice_chairman'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrationUnitContactAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=127)),
                ('city', models.CharField(max_length=63)),
                ('zip_code', models.CharField(max_length=5)),
                ('administration_unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact_address', to='administration_units.administrationunit')),
            ],
            options={
                'ordering': ('id',),
                'abstract': False,
            },
        ),
    ]
