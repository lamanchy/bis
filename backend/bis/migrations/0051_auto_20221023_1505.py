# Generated by Django 3.2.15 on 2022-10-23 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0013_rename_propagationintendedforcategory_eventintendedforcategory'),
        ('bis', '0050_alter_location_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='accessibility_from_brno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='categories.locationaccessibilitycategory'),
        ),
        migrations.AlterField(
            model_name='location',
            name='accessibility_from_prague',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='categories.locationaccessibilitycategory'),
        ),
    ]