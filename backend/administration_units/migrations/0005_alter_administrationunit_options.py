# Generated by Django 4.0.4 on 2022-05-31 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration_units', '0004_alter_brontosaurusmovement_audit_committee_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrationunit',
            options={'ordering': ('abbreviation',)},
        ),
    ]