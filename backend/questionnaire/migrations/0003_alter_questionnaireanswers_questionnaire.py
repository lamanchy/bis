# Generated by Django 3.2.15 on 2022-08-11 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_alter_questionnaire_event_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireanswers',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='questionnaire.questionnaire'),
        ),
    ]