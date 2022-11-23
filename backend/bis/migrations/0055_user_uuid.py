# Generated by Django 3.2.16 on 2022-11-23 06:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0054_user_birth_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, verbose_name='ID'),
        ),
    ]
