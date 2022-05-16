# Generated by Django 4.0.3 on 2022-03-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrationUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
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
