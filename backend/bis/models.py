from os.path import basename

from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.gis.db.models import *
from django.utils import timezone
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

from administration_units.models import AdministrationUnit, BrontosaurusMovement
from categories.models import QualificationCategory, MembershipCategory
from translation.translate import translate_model


@translate_model
class Location(Model):
    name = CharField(max_length=63)
    patron = ForeignKey('bis.User', on_delete=CASCADE, related_name='locations', null=True)
    address = CharField(max_length=255, null=True)
    gps_location = PointField(null=True)

    _import_id = CharField(max_length=15, default='')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name


@translate_model
class LocationPhoto(Model):
    location = ForeignKey(Location, on_delete=CASCADE, related_name='photos')
    photo = ImageField(upload_to='location_photos')

    @admin.display(description='Náhled')
    def photo_tag(self):
        return mark_safe(f'<img style="max-height: 10rem; max-width: 20rem" src="{self.photo.url}" />')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return basename(self.photo.name)


@translate_model
class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    first_name = CharField(max_length=63, blank=True)
    last_name = CharField(max_length=63, blank=True)
    nickname = CharField(max_length=63, blank=True)
    phone = PhoneNumberField(blank=True)
    birthday = DateField(blank=True, null=True)

    email = EmailField(unique=True)
    is_active = BooleanField(default=True)
    email_exists = BooleanField(default=True)
    date_joined = DateTimeField(default=timezone.now)

    _import_id = CharField(max_length=15, default='')

    objects = UserManager()

    @property
    def is_director(self):
        return BrontosaurusMovement.get().director == self

    @property
    def is_admin(self):
        return self in BrontosaurusMovement.get().bis_administrators.all()

    @property
    def is_office_worker(self):
        return self in BrontosaurusMovement.get().office_workers.all()

    @property
    def is_auditor(self):
        return self in BrontosaurusMovement.get().audit_committee.all()

    @property
    def is_executive(self):
        return self in BrontosaurusMovement.get().executive_committee.all()

    @property
    def is_education_member(self):
        return self in BrontosaurusMovement.get().education_members.all()

    @property
    def is_board_member(self):
        return AdministrationUnit.objects.filter(board_members=self).exists()

    def can_see_all(self):
        return self.is_director or self.is_admin or self.is_office_worker or self.is_auditor \
               or self.is_executive

    @property
    def is_staff(self):
        print(self, flush=True)
        return self.is_director or self.is_admin or self.is_office_worker or self.is_auditor \
               or self.is_executive or self.is_education_member or self.is_board_member

    @property
    def is_superuser(self):
        print(self, flush=True)
        return self.is_director or self.is_admin

    def has_usable_password(self):
        return False

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.get_name()

    @admin.display(description='Uživatel')
    def get_name(self):
        name = f'{self.first_name} {self.last_name}'
        if self.nickname:
            name = f'{self.nickname} ({name})'

        if len(name) == 1:
            return self.email

        return name

    @admin.display(description='Aktivní kvalifikace')
    def get_qualifications(self):
        return [q for q in self.qualifications.all() if q.valid_till >= timezone.now().date()]

    @admin.display(description='Aktivní členství')
    def get_memberships(self):
        return [m for m in self.memberships.all() if m.year == timezone.now().year]

    @classmethod
    def filter_queryset(cls, queryset, user):
        if user.can_see_all() or user.is_education_member:
            return queryset

        return queryset.filter(
            # ja
            Q(id=user.id)
            # lidi kolem akci od clanku kde user je board member
            | Q(participated_in_events__event__administration_unit__board_members=user)
            | Q(events_where_was_as_main_organizer__administration_unit__board_members=user)
            | Q(events_where_was_as_other_organizer__administration_unit__board_members=user)
            | Q(events_where_was_as_contact_person__event__administration_unit__board_members=user)
            # lidi kolem akci, kde user byl hlavas
            | Q(participated_in_events__event__main_organizer=user)
            | Q(events_where_was_as_other_organizer__main_organizer=user)
            | Q(events_where_was_as_contact_person__event__main_organizer=user)
            # lidi kolem akci, kde user byl other organizer
            | Q(participated_in_events__event__other_organizers=user)
            | Q(events_where_was_as_main_organizer__other_organizers=user)
            | Q(events_where_was_as_other_organizer__other_organizers=user)
            | Q(events_where_was_as_contact_person__event__other_organizers=user)
            # lidi kolem akci, kde user byl kontaktni osoba
            | Q(participated_in_events__event__propagation__contact_person=user)
            | Q(events_where_was_as_main_organizer__propagation__contact_person=user)
            | Q(events_where_was_as_other_organizer__propagation__contact_person=user)
            | Q(events_where_was_as_contact_person__event__propagation__contact_person=user)
            # orgove akci, kde user byl ucastnik
            | Q(events_where_was_as_main_organizer__record__participants=user)
            | Q(events_where_was_as_other_organizer__record__participants=user)
            | Q(events_where_was_as_contact_person__event__record__participants=user)
            # # # ostatni ucastnici akci, kde jsem byl
            # participated_in_events__participants=user,
        ).distinct()


@translate_model
class UserAddress(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='address')
    street = CharField(max_length=127)
    city = CharField(max_length=63)
    zip_code = CharField(max_length=5)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'Adresa {self.user})'


@translate_model
class Membership(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='memberships')
    category = ForeignKey(MembershipCategory, on_delete=CASCADE, related_name='memberships')
    administration_unit = ForeignKey(AdministrationUnit, on_delete=CASCADE, related_name='memberships')
    year = PositiveIntegerField()

    _import_id = CharField(max_length=15, default='')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'Člen {self.administration_unit} (rok {self.year})'


@translate_model
class Qualification(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='qualifications')
    category = ForeignKey(QualificationCategory, on_delete=CASCADE, related_name='qualifications')
    valid_since = DateField()
    valid_till = DateField()
    approved_by = ForeignKey(User, on_delete=CASCADE, related_name='approved_qualifications')

    _import_id = CharField(max_length=15, default='')

    class Meta:
        ordering = 'id',

    def __str__(self):
        return f'{self.category} (od {self.valid_since} do {self.valid_till})'
