# Generated by Django 4.0.3 on 2022-03-23 15:35

from django.conf import settings
import django.contrib.auth.models
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('categories', '0001_initial'),
        ('administration_units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=63)),
                ('last_name', models.CharField(blank=True, max_length=63)),
                ('nickname', models.CharField(blank=True, max_length=63)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('gps_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_till', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='categories.qualificationcategory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='qualification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('administration_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='administration_units.administrationunit')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='categories.membershipcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='LocationPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='location_photos')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='bis.location')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('is_canceled', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateField()),
                ('is_internal', models.BooleanField(default=False)),
                ('number_of_sub_events', models.PositiveIntegerField(default=1)),
                ('administration_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='administration_units.administrationunit')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='bis.location')),
                ('main_organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_where_was_as_main_organizer', to=settings.AUTH_USER_MODEL)),
                ('other_organizers', models.ManyToManyField(blank=True, related_name='events_where_was_as_other_organizer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
