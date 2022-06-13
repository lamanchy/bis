# Generated by Django 4.0.5 on 2022-06-13 06:24
from os.path import join

from django.contrib.gis.gdal import DataSource
from django.db import migrations

from project.settings import BASE_DIR


def migrate(apps, schema_editor):
    Region = apps.get_model('other', 'Region')
    path = join(BASE_DIR, 'other', 'region_borders', 'SPH_KRAJ.shp')
    data = DataSource(path)

    for item in data[0]:
        Region.objects.update_or_create(
            name=item.get('NAZEV_NUTS'),
            defaults=dict(
                area=item.geom.wkt
            ))


class Migration(migrations.Migration):
    dependencies = [
        ('other', '0004_region'),
    ]

    operations = [
        migrations.RunPython(migrate, migrations.RunPython.noop)
    ]
