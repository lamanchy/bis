# Generated by Django 3.2.17 on 2023-02-19 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_book', '0003_auto_20230211_1809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('-created_at',)},
        ),
    ]
