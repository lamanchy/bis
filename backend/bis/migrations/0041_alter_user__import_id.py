# Generated by Django 3.2.15 on 2022-09-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0040_auto_20220913_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='_import_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
