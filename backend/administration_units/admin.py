from django.contrib import admin
from django.utils.safestring import mark_safe
from more_admin_filters import MultiSelectRelatedDropdownFilter
from nested_admin.nested import NestedModelAdmin, NestedTabularInline
from solo.admin import SingletonModelAdmin

from administration_units.models import AdministrationUnit, BrontosaurusMovement, AdministrationUnitAddress, \
    AdministrationUnitContactAddress
from bis.admin_helpers import EditableByAdminOnlyMixin, IsAdministrationUnitActiveFilter
from bis.helpers import show_history


class AdministrationUnitAddressAdmin(EditableByAdminOnlyMixin, NestedTabularInline):
    model = AdministrationUnitAddress


class AdministrationUnitContactAddressAdmin(EditableByAdminOnlyMixin, NestedTabularInline):
    model = AdministrationUnitContactAddress


@admin.register(AdministrationUnit)
class AdministrationUnitAdmin(EditableByAdminOnlyMixin, NestedModelAdmin):
    list_display = 'abbreviation', 'is_active', 'address', 'phone', 'get_email', 'www', 'chairman', 'category'
    search_fields = 'abbreviation', 'name', 'address__city', 'address__street', 'address__zip_code', 'phone', 'email'
    list_filter = IsAdministrationUnitActiveFilter, 'category', 'is_for_kids', \
                  ('address__region', MultiSelectRelatedDropdownFilter)

    autocomplete_fields = 'chairman', 'vice_chairman', 'manager', 'board_members'

    exclude = '_import_id', '_history'
    list_select_related = 'address', 'chairman', 'category'
    readonly_fields = 'history',

    inlines = AdministrationUnitAddressAdmin, AdministrationUnitContactAddressAdmin

    @admin.display(description='Je aktivní', boolean=True)
    def is_active(self, obj):
        return obj.existed_till is None

    @admin.display(description='Historie')
    def history(self, obj):
        return show_history(obj._history)

    @admin.display(description='E-mail')
    def get_email(self, obj):
        if not obj.email: return None
        name, host = obj.email.split('@')
        return mark_safe(f'{name}<br>@{host}')


@admin.register(BrontosaurusMovement)
class BrontosaurusMovementAdmin(EditableByAdminOnlyMixin, SingletonModelAdmin):
    filter_horizontal = 'bis_administrators', 'office_workers', 'audit_committee', \
                        'executive_committee', 'education_members',

    autocomplete_fields = 'director', 'finance_director', 'bis_administrators', 'office_workers', 'audit_committee', \
                          'executive_committee', 'education_members'
    readonly_fields = 'history',
    exclude = '_history',

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Historie')
    def history(self, obj):
        return show_history(obj._history)

