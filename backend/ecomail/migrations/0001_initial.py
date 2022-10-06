# Generated by Django 3.2.15 on 2022-09-22 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Kontakt',
                'verbose_name_plural': 'Kontakty',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ContactLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField()),
                ('log', models.TextField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecomail.contact')),
            ],
            options={
                'verbose_name': 'Záznam aktivity kontaktu',
                'verbose_name_plural': 'Záznamy aktivity kontaktu',
                'ordering': ['id'],
            },
        ),
    ]