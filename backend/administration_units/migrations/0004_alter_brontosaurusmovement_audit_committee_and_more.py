# Generated by Django 4.0.4 on 2022-05-31 12:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration_units', '0003_delete_administrationunitmember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='audit_committee',
            field=models.ManyToManyField(help_text='Vidí vše, nemohou editovat', related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='bis_administrators',
            field=models.ManyToManyField(help_text='Mají veškeré oprávnění', related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='education_members',
            field=models.ManyToManyField(help_text='Vidí pouze uživatele a mohou je editovat pouze kvalifikaci', related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='executive_committee',
            field=models.ManyToManyField(help_text='Vidí vše, nemohou editovat', related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='office_workers',
            field=models.ManyToManyField(help_text='Mohou měnit vše kromě základních oprávnění', related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
