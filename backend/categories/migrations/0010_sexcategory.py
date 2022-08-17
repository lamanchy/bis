# Generated by Django 3.2.15 on 2022-08-17 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0009_alter_healthinsurancecompany_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SexCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
