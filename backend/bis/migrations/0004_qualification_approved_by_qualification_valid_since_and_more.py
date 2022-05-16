# Generated by Django 4.0.3 on 2022-05-09 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0003_alter_useraddress_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualification',
            name='approved_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='approved_qualifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='qualification',
            name='valid_since',
            field=models.DateField(default=django.utils.datetime_safe.date.today),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='valid_till',
            field=models.DateField(default=django.utils.datetime_safe.date.today),
        ),
    ]
