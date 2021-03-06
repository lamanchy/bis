# Generated by Django 4.0.4 on 2022-05-16 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('administration_units', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='audit_committee',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='bis_administrators',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='director',
            field=models.ForeignKey(help_text='Má veškerá oprávnění', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='education_members',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='executive_committee',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brontosaurusmovement',
            name='office_workers',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrationunitmember',
            name='administration_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration_units.administrationunit'),
        ),
        migrations.AddField(
            model_name='administrationunitmember',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.administrationunitboardmembercategory'),
        ),
        migrations.AddField(
            model_name='administrationunitmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrationunitaddress',
            name='administration_unit',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='administration_units.administrationunit'),
        ),
        migrations.AddField(
            model_name='administrationunit',
            name='board_members',
            field=models.ManyToManyField(related_name='administration_units', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrationunit',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administration_units', to='categories.administrationunitcategory'),
        ),
        migrations.AddField(
            model_name='administrationunit',
            name='chairman',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrationunit',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
