from admin_auto_filters.filters import AutocompleteFilterFactory
from admin_numeric_filter.admin import NumericFilterModelAdmin
from django.contrib.auth.models import Group
from django.contrib.gis.admin import OSMGeoAdmin
from more_admin_filters import MultiSelectRelatedDropdownFilter, MultiSelectDropdownFilter
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedTabularInline, NestedStackedInline, NestedModelAdminMixin
from rangefilter.filters import DateRangeFilter
from rest_framework.authtoken.models import TokenProxy

from bis.admin_helpers import ActiveQualificationFilter, ActiveMembershipFilter, FilterQuerysetMixin, \
    EditableByBoardMixin, MembershipsYearFilter, AgeFilter, IsChairmanFilter, IsViceChairmanFilter, IsManagerFilter, \
    IsBoardMemberFilter
from bis.models import *
from opportunities.models import OfferedHelp
from other.models import DuplicateUser

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)


class LocationPhotosAdmin(NestedTabularInline):
    model = LocationPhoto
    readonly_fields = 'photo_tag',


@admin.register(Location)
class LocationAdmin(EditableByBoardMixin, OSMGeoAdmin):
    inlines = LocationPhotosAdmin,
    search_fields = 'name',
    autocomplete_fields = 'patron', 'contact_person'
    exclude = '_import_id',

    list_filter = 'program', 'for_beginners', 'is_full', 'is_unexplored', \
                  ('accessibility_from_prague', MultiSelectRelatedDropdownFilter), \
                  ('accessibility_from_brno', MultiSelectRelatedDropdownFilter), \
                  ('region', MultiSelectRelatedDropdownFilter)


class MembershipAdmin(EditableByBoardMixin, NestedTabularInline):
    model = Membership
    extra = 0

    autocomplete_fields = 'administration_unit',

    exclude = '_import_id',


class QualificationAdmin(NestedTabularInline):
    model = Qualification
    fk_name = 'user'
    extra = 0

    autocomplete_fields = 'approved_by',

    exclude = '_import_id',


class UserEmailAdmin(SortableHiddenMixin, NestedTabularInline):
    model = UserEmail
    sortable_field_name = 'order'
    extra = 0


class DuplicateUserAdminInline(NestedTabularInline):
    model = DuplicateUser
    fk_name = 'user'
    autocomplete_fields = 'other',
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class UserAddressAdmin(NestedTabularInline):
    model = UserAddress


class UserContactAddressAdmin(NestedTabularInline):
    model = UserContactAddress


class UserOfferedHelpAdmin(NestedStackedInline):
    model = OfferedHelp


@admin.register(User)
class UserAdmin(EditableByBoardMixin, FilterQuerysetMixin, NestedModelAdminMixin, NumericFilterModelAdmin):
    readonly_fields = 'is_superuser', 'last_login', 'date_joined', 'get_emails', 'get_events_where_was_organizer', 'get_participated_in_events'
    exclude = 'groups', 'user_permissions', 'password', 'is_superuser', '_str'

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'nickname', 'get_emails', 'phone', 'birthday', 'close_person')
        }),
        ('Ud??losti', {
            'fields': ('get_events_where_was_organizer', 'get_participated_in_events')
        }),
        ('Intern?? data', {
            'fields': ('is_active', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        })
    )

    autocomplete_fields = 'close_person',

    list_display = 'get_name', 'birthday', 'address', 'contact_address', 'get_emails', 'phone', 'get_qualifications', 'get_memberships'
    list_filter = ActiveMembershipFilter, \
                  AutocompleteFilterFactory('??len ??l??nku', 'memberships__administration_unit'), \
                  ('memberships__year', MembershipsYearFilter), \
                  AgeFilter, \
                  ActiveQualificationFilter, \
                  ('qualifications__category', MultiSelectRelatedDropdownFilter), \
                  ('date_joined', DateRangeFilter), ('birthday', DateRangeFilter), \
                  ('participated_in_events__event__start', DateRangeFilter), \
                  ('events_where_was_organizer__start', DateRangeFilter), \
                  ('events_where_was_as_main_organizer__start', DateRangeFilter), \
                  IsChairmanFilter, \
                  IsViceChairmanFilter, \
                  IsManagerFilter, \
                  IsBoardMemberFilter, \
                  ('offers__programs', MultiSelectRelatedDropdownFilter), \
                  ('offers__organizer_roles', MultiSelectRelatedDropdownFilter), \
                  ('offers__team_roles', MultiSelectRelatedDropdownFilter), \
                  ('address__region', MultiSelectRelatedDropdownFilter)

    search_fields = 'emails__email', 'phone', 'first_name', 'last_name', 'nickname'
    list_select_related = 'address', 'contact_address'

    def get_inlines(self, request, obj):
        inlines = [UserAddressAdmin, UserContactAddressAdmin,
                   UserOfferedHelpAdmin,
                   QualificationAdmin, MembershipAdmin,
                   DuplicateUserAdminInline]
        if request.user.is_superuser:
            inlines.append(UserEmailAdmin)
        return inlines

    def get_rangefilter_participated_in_events__event__start_title(self, request, field_path):
        return 'Jeli na akci v obdob??'

    def get_rangefilter_events_where_was_organizer__start_title(self, request, field_path):
        return 'Organizovali akci v obdob??'

    def get_rangefilter_events_where_was_as_main_organizer__start_title(self, request, field_path):
        return 'Vedli akci v obdob??'

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_education_member:
            return super().get_readonly_fields(request, obj)

        result = []
        for fieldset in self.fieldsets:
            for field in fieldset[1]['fields']:
                result.append(field)
        return result

    def has_change_permission(self, request, obj=None):
        return self.has_add_permission(request, obj) or request.user.is_education_member

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('memberships', 'qualifications', 'emails',
                                                              'events_where_was_organizer',
                                                              'participated_in_events__event')
