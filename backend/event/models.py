from os.path import basename

from django.conf import settings
from django.contrib import admin
from django.contrib.gis.db.models import *
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from administration_units.models import AdministrationUnit
from bis.models import Location, User
from categories.models import GrantCategory, PropagationIntendedForCategory, DietCategory, \
    EventCategory, EventProgramCategory
from translation.translate import translate_model


@translate_model
class Event(Model):
    # general
    name = CharField(max_length=63)
    is_canceled = BooleanField(default=False)
    start = DateTimeField()
    end = DateField()
    number_of_sub_events = PositiveIntegerField(default=1)
    location = ForeignKey(Location, on_delete=CASCADE, related_name='events', null=True)

    category = ForeignKey(EventCategory, on_delete=CASCADE, related_name='events')
    program = ForeignKey(EventProgramCategory, on_delete=CASCADE, related_name='events', blank=True, null=True)

    administration_units = ManyToManyField(AdministrationUnit, related_name='events')
    main_organizer = ForeignKey(User, on_delete=CASCADE, related_name='events_where_was_as_main_organizer', null=True)
    other_organizers = ManyToManyField(User, related_name='events_where_was_organizer', blank=True)

    is_attendance_list_required = BooleanField(default=False)
    is_internal = BooleanField(default=False)
    internal_note = TextField(blank=True)

    _import_id = CharField(max_length=15, default='')
    duration = PositiveIntegerField()

    class Meta:
        ordering = '-start',
        app_label = 'bis'

    def __str__(self):
        return self.name

    def is_volunteering(self):
        return self.category.slug.startswith('public__volunteering')

    @admin.display(description='Termín akce')
    def get_date(self):
        time = timezone.localtime(self.start)
        start_date = timezone.localdate(self.start)
        end_date = self.end
        result = f'{self.end.day}. {self.end.month}. {self.end.year}'

        if start_date != end_date:
            result = '- ' + result
            if start_date.year != end_date.year:
                result = f"{start_date.year}. " + result
            if start_date.month != end_date.month:
                result = f"{start_date.month}. " + result
            if start_date.day != end_date.day:
                result = f"{start_date.day}. " + result

        # if time.hour != 0:
        #     result += f' {time.hour}:{time.minute:02d}'
        return result

    @classmethod
    def filter_queryset(cls, queryset, user):
        ids = set()
        for query in [
            Q(administration_units__board_members=user),
            Q(other_organizers=user),
            Q(record__participants=user),
        ]:
            ids = ids.union(queryset.filter(query).order_by().values_list('id', flat=True))
        return Event.objects.filter(id__in=ids)


@translate_model
class EventFinance(Model):
    event = OneToOneField(Event, related_name='finance', on_delete=CASCADE)

    bank_account_number = CharField(max_length=63, blank=True)

    grant_category = ForeignKey(GrantCategory, on_delete=CASCADE, related_name='events', null=True, blank=True)
    grant_amount = PositiveIntegerField(null=True, blank=True)
    total_event_cost = PositiveIntegerField(null=True, blank=True)
    budget = FileField(upload_to='budgets', blank=True)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'Finance k události {self.event}'


@translate_model
class EventFinanceReceipt(Model):
    finance = ForeignKey(EventFinance, on_delete=CASCADE, related_name='receipts')
    receipt = FileField(upload_to='receipts')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return basename(self.receipt.name)


@translate_model
class EventPropagation(Model):
    event = OneToOneField(Event, related_name='propagation', on_delete=CASCADE)

    is_shown_on_web = BooleanField()

    minimum_age = PositiveIntegerField(null=True, blank=True)
    maximum_age = PositiveIntegerField(null=True, blank=True)
    cost = PositiveIntegerField()
    discounted_cost = PositiveIntegerField(blank=True, null=True)
    intended_for = ForeignKey(PropagationIntendedForCategory, on_delete=CASCADE, related_name='events')
    accommodation = CharField(max_length=255)
    diets = ManyToManyField(DietCategory, related_name='events', blank=True)
    organizers = CharField(max_length=255)
    web_url = URLField(blank=True)
    _contact_url = URLField(blank=True)

    invitation_text_introduction = HTMLField()
    invitation_text_practical_information = HTMLField()
    invitation_text_work_description = HTMLField(blank=True)
    invitation_text_about_us = HTMLField(blank=True)
    # propagation_images as Model below

    contact_person = ForeignKey(User, on_delete=CASCADE, related_name='events_where_was_as_contact_person', null=True)
    contact_name = CharField(max_length=63, blank=True)
    contact_phone = PhoneNumberField(blank=True)
    contact_email = EmailField(blank=True)

    def clean(self):
        if self.event.is_volunteering() and not self.invitation_text_work_description:
            raise ValidationError('Popis dobrovolnické pomoci je povinný pro dobrovolnické akce')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not settings.SKIP_VALIDATION: self.clean()
        self.contact_email = self.contact_email.lower()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'Propagace k události {self.event}'


@translate_model
class VIPEventPropagation(Model):
    event_propagation = OneToOneField(EventPropagation, related_name='vip_propagation', on_delete=CASCADE)

    goals_of_event = TextField()
    program = TextField()
    short_invitation_text = TextField(max_length=200)

    rover_propagation = BooleanField(default=False)


@translate_model
class EventRegistration(Model):
    event = OneToOneField(Event, related_name='registration', on_delete=CASCADE)

    is_registration_required = BooleanField(default=True)
    is_event_full = BooleanField(default=False)

    # filled answers as part of questionary

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'Registrace k události {self.event}'


@translate_model
class EventRecord(Model):
    event = OneToOneField(Event, related_name='record', on_delete=CASCADE)

    total_hours_worked = PositiveIntegerField(null=True, blank=True)
    working_hours = PositiveSmallIntegerField(null=True, blank=True)
    working_days = PositiveSmallIntegerField(null=True, blank=True)
    comment_on_work_done = TextField(blank=True)
    attendance_list = ImageField(upload_to='attendance_lists', null=True, blank=True)
    participants = ManyToManyField(User, 'participated_in_events', blank=True)
    number_of_participants = PositiveIntegerField(null=True, blank=True)
    number_of_participants_under_26 = PositiveIntegerField(null=True, blank=True)

    def clean(self):
        if self.event.is_attendance_list_required and not self.attendance_list:
            raise ValidationError('Prezenční listina není vyplněna')

        if self.event.is_volunteering() and not self.total_hours_worked:
            raise ValidationError('Odpracováno člověkohodin nevyplněno')

        if (self.event.duration or 0) > 1 and self.event.is_volunteering():
            if not self.working_hours:
                raise ValidationError('Odpracovaných hodin denně nevyplněno')
            if not self.working_days:
                raise ValidationError('Počet pracovních dní nevyplněno')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not settings.SKIP_VALIDATION: self.clean()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = '-event__start',

    def __str__(self):
        return f'Záznam k události {self.event}'


@translate_model
class EventPropagationImage(Model):
    propagation = ForeignKey(EventPropagation, on_delete=CASCADE, related_name='images')
    order = PositiveIntegerField()
    image = ImageField(upload_to='event_propagation_images', max_length=200)

    @admin.display(description='Náhled')
    def image_tag(self):
        return mark_safe(f'<img style="max-height: 10rem; max-width: 20rem" src="{self.image.url}" />')

    class Meta:
        ordering = 'order',

    def __str__(self):
        return basename(self.image.name)

    @property
    def url(self):
        return settings.FULL_HOSTNAME + self.image.url


@translate_model
class EventPhoto(Model):
    record = ForeignKey(EventRecord, on_delete=CASCADE, related_name='photos')
    photo = ImageField(upload_to='event_photos')

    @admin.display(description='Náhled')
    def photo_tag(self):
        return mark_safe(f'<img style="max-height: 10rem; max-width: 20rem" src="{self.photo.url}" />')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return basename(self.photo.name)
