# Generated by Django 4.0.5 on 2022-06-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0011_delete_duplicateuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
