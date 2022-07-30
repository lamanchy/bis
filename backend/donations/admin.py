from admin_auto_filters.filters import AutocompleteFilterFactory
from admin_numeric_filter.admin import RangeNumericFilter
from django.contrib.messages import INFO, ERROR
from django.http import HttpResponseRedirect
from django.urls import reverse
from more_admin_filters import MultiSelectRelatedDropdownFilter
from nested_admin.nested import NestedModelAdmin, NestedTabularInline
from rangefilter.filters import DateRangeFilter
from solo.admin import SingletonModelAdmin

from bis.admin_helpers import HasDonorFilter, FirstDonorsDonationFilter, LastDonorsDonationFilter, \
    RecurringDonorWhoStoppedFilter, AnnotateDonationsCount, DonationSumAmountFilter
from bis.admin_permissions import ReadOnlyMixin, EditableByAdminOnlyMixin, EditableByOfficeMixin
from donations.helpers import upload_bank_records
from donations.models import UploadBankRecords, Donor, Donation, VariableSymbol
from event.models import *


@admin.register(Donation)
class DonationAdmin(ReadOnlyMixin, NestedModelAdmin):
    autocomplete_fields = 'donor',
    list_display = '__str__', 'donor', 'donated_at', 'donation_source', 'info'
    list_filter = ('amount', RangeNumericFilter), ('donated_at', DateRangeFilter), HasDonorFilter, \
                  ('donation_source', MultiSelectRelatedDropdownFilter)
    exclude = '_import_id', '_variable_symbol'

    list_select_related = 'donor__user', 'donation_source'

    def has_delete_permission(self, request, obj=None):
        return obj and not obj.donor


class DonationAdminInline(NestedTabularInline):
    model = Donation

    def has_add_permission(self, request, obj): return False

    def has_change_permission(self, request, obj=None): return False

    def has_delete_permission(self, request, obj=None): return False


class VariableSymbolInline(NestedTabularInline):
    model = VariableSymbol
    extra = 0

    def has_change_permission(self, request, obj=None): return False


@admin.register(Donor)
class DonorAdmin(EditableByOfficeMixin, NestedModelAdmin):
    list_display = 'user', 'subscribed_to_newsletter', 'is_public', \
                   'regional_center_support', 'basic_section_support', \
                   'date_joined', 'get_donations_sum'

    list_select_related = 'user', 'regional_center_support', 'basic_section_support'
    inlines = VariableSymbolInline, DonationAdminInline,
    search_fields = 'user__emails__email', 'user__phone', 'user__first_name', 'user__last_name', 'user__nickname',
    list_filter = 'subscribed_to_newsletter', 'is_public', 'has_recurrent_donation', \
                  ('date_joined', DateRangeFilter), \
                  AutocompleteFilterFactory('Podporující RC', 'regional_center_support'), \
                  AutocompleteFilterFactory('Podporující ZČ', 'basic_section_support'), \
                  ('donations__donated_at', FirstDonorsDonationFilter), \
                  ('donations__donated_at', LastDonorsDonationFilter), \
                  ('donations__donated_at', AnnotateDonationsCount), \
                  ('donations__amount', DonationSumAmountFilter), \
                  RecurringDonorWhoStoppedFilter

    autocomplete_fields = 'regional_center_support', 'basic_section_support', 'user'

    def get_readonly_fields(self, request, obj=None):
        if obj: return 'user', 'get_donations_sum'
        return 'get_donations_sum',

    def save_formset(self, request, form, formset, change):
        if formset.model is Donation:
            formset.new_objects = []
            formset.changed_objects = []
            formset.deleted_objects = []
            return
        super().save_formset(request, form, formset, change)

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .annotate(first_donation=Min('donations__donated_at')) \
            .annotate(last_donation=Max('donations__donated_at')) \
            .annotate(donations_sum=Sum('donations__amount'))

    @admin.display(description='Suma darů')
    def get_donations_sum(self, obj):
        if hasattr(self, 'donations_sum_cache'):
            return getattr(self, 'donations_sum_cache')[obj.id]
        return obj.donations_sum


@admin.register(UploadBankRecords)
class UploadBankRecordsAdmin(EditableByAdminOnlyMixin, SingletonModelAdmin):

    def save_model(self, request, obj, form, change):
        try:
            upload_bank_records(obj.file.file)
            self.message_user(request, "Záznamy úspěšně nahrány", INFO)
        except AssertionError as e:
            self.message_user(request, str(e), ERROR)

    def response_change(self, request, obj):
        return HttpResponseRedirect(reverse('admin:donations_uploadbankrecords_changelist'))

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['show_save_and_continue'] = False
        context['show_save_and_add_another'] = False
        context['show_delete'] = False
        return super().render_change_form(request, context, add, change, form_url, obj)
