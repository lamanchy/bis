# Generated by Django 4.0.4 on 2022-05-16 15:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrationUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=63)),
                ('is_for_kids', models.BooleanField()),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('www', models.URLField(null=True)),
                ('ic', models.CharField(max_length=15, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=63, null=True)),
                ('existed_since', models.DateField(null=True)),
                ('existed_till', models.DateField(blank=True, null=True)),
                ('_import_id', models.CharField(default='', max_length=15)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AdministrationUnitAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=127)),
                ('city', models.CharField(max_length=63)),
                ('zip_code', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AdministrationUnitMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('since', models.DateTimeField()),
                ('till', models.DateTimeField()),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='BrontosaurusMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
