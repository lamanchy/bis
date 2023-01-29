# Generated by Django 3.2.16 on 2023-01-29 10:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration_units', '0003_alter_administrationunit_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrationunit',
            name='abbreviation',
            field=models.CharField(help_text='Běžně užívaný název, např. Zvonek, Orchis...', max_length=63, unique=True),
        ),
        migrations.AlterField(
            model_name='administrationunit',
            name='name',
            field=models.CharField(help_text='Název z rejstříku, např. ZČ HB Zvonek', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='brontosaurusmovement',
            name='education_members',
            field=models.ManyToManyField(blank=True, help_text='Vidí pouze uživatele a mohou editovat pouze jejich kvalifikaci', related_name='_administration_units_brontosaurusmovement_education_members_+', to=settings.AUTH_USER_MODEL),
        ),
    ]