# Generated by Django 3.2.17 on 2023-02-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_book_categories', '0005_auto_20230218_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelengthcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='locationcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='materialrequirementcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='mentalcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='organizersnumbercategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='participantagecategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='participantnumbercategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='physicalcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='preparationlengthcategory',
            name='emoji',
            field=models.CharField(max_length=3),
        ),
    ]
